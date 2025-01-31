from flask_restx import Resource
from flask import request,jsonify
from app.appMain.Models.users import Users
from app.appMain.Models.itineraries import Itinerary
from app.appMain.dto.itineraries import ItineraryDto
from app.appMain import db
from app.appMain.Models.wishlist import Wishlist
from datetime import datetime
from app.appMain.Models import Itinerary, Destination, Accommodation, Activity
from app.appMain.Models.pictures import Picture
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
import json
import uuid
import traceback
from uuid import UUID
from flask_jwt_extended import JWTManager, jwt_required,create_access_token


createtitineraryapi_blueprint = ItineraryDto.createitineraryapi
getitinerariesapi_blueprint = ItineraryDto.getitinerariesapi
updateitinerariesapi_blueprint = ItineraryDto.updateitinerariesapi
deleteitinerariesapi_blueprint = ItineraryDto.deleteitinerariesapi
getallitinerariesapi_blueprint = ItineraryDto.getallitinerariesapi
itineraries_blueprint= ItineraryDto.itinerariesapi
wishlistapi_blueprint = ItineraryDto.wishlistitinerariesapi

UPLOAD_FOLDER = '/home/lilly/Travelmate/Demo/src/assets'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

createtitineraryapi_blueprint = ItineraryDto.createitineraryapi

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@createtitineraryapi_blueprint.route('', methods=['POST'])
class CreateItinerary(Resource):
    # @jwt_required()
    def post(self):
        # Debugging: Log the form data and files
        print("Request Files:", request.files)
        print("Request Form Data:", request.form)

        if 'files' not in request.files:
            return {'error': "No files found"}, 400

        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return {'error': 'No files selected'}, 400

        filenames = []
        for file in files:
            if file.filename == '':
                continue
            if not allowed_file(file.filename):
                return {'error': f'File type not allowed for {file.filename}'}, 400
            filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{secure_filename(file.filename)}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                file.save(file_path)
                filenames.append(filename)
            except Exception as e:
                return {'error': f'Error saving file {filename}: {str(e)}'}, 500

        data = request.form
        user_id = data.get('userId')
        if not user_id:
            return {"error": "userId is required."}, 400
        if not data.get('itinerary_name') or not data.get('start_date') or not data.get('end_date') or not data.get('estimated_cost'):
            return {"error": "itinerary_name, start date, end date, and estimated_cost are required."}, 400

        try:
            user_id = UUID(user_id)  # Validate user_id format
        except ValueError:
            return {"error": "Invalid userId format."}, 400

        user = Users.query.filter_by(user_id=user_id).first()
        if not user:
            return {"error": "Invalid user"}, 400

        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

        if end_date <= start_date:
            return {"error": "The end date must be later than the start date."}, 400

        duration = (end_date - start_date).days

        # Parse JSON fields with error handling
        try:
            destinations = json.loads(data.get('destinations', '[]'))
        except json.JSONDecodeError:
            return {"error": "Invalid destinations format."}, 400

        try:
            accommodations = json.loads(data.get('accommodations', '[]'))
        except json.JSONDecodeError:
            return {"error": "Invalid accommodations format."}, 400

        try:
            activities = json.loads(data.get('activities', '[]'))
        except json.JSONDecodeError:
            return {"error": "Invalid activities format."}, 400

        try:
            new_itinerary = Itinerary(
                user_id=user_id,
                itinerary_name=data['itinerary_name'],
                description=data.get('description', ''),
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                estimated_cost=float(data.get('estimated_cost'))
            )
            db.session.add(new_itinerary)
            db.session.commit()

            # Add pictures associated with the itinerary
            for filename in filenames:
                new_picture = Picture(
                    filename=filename,
                    itinerary_id=new_itinerary.itinerary_id
                )
                db.session.add(new_picture)
            db.session.commit()

            # Add destinations
            for dest in destinations:
                new_destination = Destination(
                    itinerary=new_itinerary,
                    location=dest['location'],
                    duration=dest['duration'],
                    notes=dest.get('notes', '')
                )
                db.session.add(new_destination)

            # Add accommodations
            for accommodation in accommodations:
                accommodation_obj = Accommodation(
                    itinerary=new_itinerary,
                    hotel_name=accommodation['hotel_name'],
                    check_in_date=accommodation['check_in_date'],
                    check_out_date=accommodation['check_out_date'],
                    address=accommodation.get('address', ''),
                    notes=accommodation.get('notes', '')
                )
                db.session.add(accommodation_obj)

            # Add activities
            for activity in activities:
                activity_obj = Activity(
                    itinerary=new_itinerary,
                    activity_name=activity['activity_name'],
                    date=activity['date'],
                    time=activity.get('time') if activity.get('time') != '' else None,
                    notes=activity.get('notes', '')
                )
                db.session.add(activity_obj)

            db.session.commit()

            new_itinerary_data = new_itinerary.to_dict()
            new_itinerary_data['pictures'] = [picture.to_dict() for picture in new_itinerary.pictures]

            return {
                "message": "Itinerary created successfully!",
                "itinerary_id": new_itinerary.itinerary_id,
                "itinerary": new_itinerary_data
            }, 201

        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            for filename in filenames:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, filename))
                except OSError:
                    pass
            return {"error": f"An error occurred: {str(e)}"}, 500



@updateitinerariesapi_blueprint.route('', methods=['PUT'])
class UpdateItineraries(Resource):
    def put(self):
        data = request.get_json()
        email = data.get('email')
        itinerary_id = data.get('itinerary_id')  

        # Get user_id based on email
        user = Users.query.filter_by(email=email).first()
        if not user:
            return {'message': 'User not found'}, 404
        
        # Fetch the specific itinerary by ID for the user
        itinerary = Itinerary.query.filter_by(itinerary_id=itinerary_id, user_id=user.user_id).first()
        if not itinerary:
            return {'message': 'Itinerary not found'}, 404

        # Update the itinerary fields
        itinerary_name = data.get('itinerary_name')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        duration = data.get('duration')
        estimated_cost = data.get('estimated_cost')

        if itinerary_name:
            itinerary.itinerary_name = itinerary_name
        if description:
            itinerary.description = description
        if start_date:
            itinerary.start_date = start_date
        if end_date:
            itinerary.end_date = end_date
        if duration:
            itinerary.duration = duration
        if estimated_cost:
            itinerary.estimated_cost = estimated_cost

        itinerary.updated_at = db.func.now()

        try:
            db.session.commit()
            return {'message': 'Itinerary updated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to update itinerary', 'error': str(e)}, 500


@wishlistapi_blueprint.route('', methods=['POST', 'GET', 'DELETE'])
class WishlistResource(Resource):
    def post(self):
        data = request.json
        
        itinerary_id = data.get('itinerary_id')
        user_id = data.get('user_id')
        email = data.get('email')

        if not all([itinerary_id, user_id, email]):
            return {"message": "Itinerary ID, User ID, and Email are required"}, 400

        # Check if the itinerary is already in the wishlist for this user
        existing_entry = db.session.query(Wishlist).filter_by(
            itinerary_id=itinerary_id,
            user_id=user_id,
            email=email
        ).first()

        if existing_entry:
            return {"message": "Itinerary is already in the wishlist"}, 409  # Conflict response code

        # Add the new wishlist entry
        new_wishlist_entry = Wishlist(itinerary_id=itinerary_id, user_id=user_id, email=email)

        try:
            db.session.add(new_wishlist_entry)  # Add the entry to the session
            db.session.commit()  # Commit the transaction
            return {"message": "Itinerary added to wishlist!"}, 201  # Return success response
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return {"message": "Error adding to wishlist", "error": str(e)}, 500  # Return error response

        
    def get(self):
        email = request.args.get('email')
        if not email:
            return {'error': 'Email parameter is missing.'}, 400
        
        # Query the wishlist for the given email
        wishlisted_items = db.session.query(Wishlist).filter_by(email=email).all()
        
        if not wishlisted_items:
            return {'wishlistedItineraries': []}, 200
        
        # Prepare the response data
        result = []
        for item in wishlisted_items:
            # Fetch the corresponding itinerary details
            itinerary = db.session.query(Itinerary).filter_by(itinerary_id=item.itinerary_id).first()
            if itinerary:
                # Serialize destinations
                destinations_data = []
                for destination in itinerary.destinations:
                    destinations_data.append({
                        'destination_id': str(destination.destination_id),  # Assuming you have an ID
                        'destination_name': destination.location 
                    })
                
                result.append({
                    'wishlist_id': str(item.wishlist_id),  # Convert UUID to string
                    'itinerary_id': str(item.itinerary_id),  # Convert UUID to string
                    'user_id': str(item.user_id),  # Convert UUID to string if user_id is also a UUID
                    'itinerary_name': itinerary.itinerary_name,  # Assuming 'name' is a field in the Itinerary model
                    'description':itinerary.description,
                    'destinations': destinations_data  # Include the serialized destinations
                })
        
        return {'wishlistedItineraries': result}, 200
    def delete(self):
        data = request.json
        wishlist_id = data.get('wishlist_id')
        
        if not wishlist_id:
            return {"message": "Wishlist ID is required"}, 400

        # Attempt to find the wishlist entry
        wishlist_entry = db.session.query(Wishlist).filter_by(wishlist_id=wishlist_id).first()

        if not wishlist_entry:
            return {"message": "Wishlist entry not found"}, 404

        try:
            db.session.delete(wishlist_entry)  # Delete the wishlist entry
            db.session.commit()  # Commit the transaction
            return {"message": "Itinerary removed from wishlist!"}, 200  # Return success response
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            return {"message": "Error removing from wishlist", "error": str(e)}, 500  # Return error response

@getallitinerariesapi_blueprint.route('', methods=['GET'])
class GetPublicItineraries(Resource):
    def get(self):
        try:
            user_id = request.args.get('user_id')  # Retrieve user_id from query parameters

            if not user_id:
                return {
                    'success': False,
                    'message': 'User ID not provided'
                }, 400

            public_itineraries = Itinerary.query.filter(Itinerary.user_id != user_id).all()

            result = []
            for itinerary in public_itineraries:
                user = Users.query.filter_by(user_id = itinerary.user_id).first()

                destinations = [
                    destination.location for destination in itinerary.destinations
                ] if itinerary.destinations else []

                accommodations = [
                    {
                        'hotel_name': accommodation.hotel_name,
                        'check_in_date': accommodation.check_in_date.strftime('%Y-%m-%d') if accommodation.check_in_date else None,
                        'check_out_date': accommodation.check_out_date.strftime('%Y-%m-%d') if accommodation.check_out_date else None,
                        'address': accommodation.address,
                        'notes': accommodation.notes
                    } for accommodation in itinerary.accommodations
                ] if itinerary.accommodations else []

                activities = [
                    {
                        'activity_name': activity.activity_name,
                        'date': activity.date.strftime('%Y-%m-%d') if activity.date else None,
                        'time': activity.time.strftime('%H:%M') if activity.time else None,
                        'notes': activity.notes
                    } for activity in itinerary.activities
                ] if itinerary.activities else []

                result.append({
                    'itinerary_id': itinerary.itinerary_id,
                    'itinerary_name': itinerary.itinerary_name,
                    'description': itinerary.description,
                    'start_date': itinerary.start_date.strftime('%Y-%m-%d') if itinerary.start_date else None,
                    'end_date': itinerary.end_date.strftime('%Y-%m-%d') if itinerary.end_date else None,
                    'destinations': [destination.location for destination in itinerary.destinations] if itinerary.destinations else [],
                    'accommodations': accommodations,
                    'activities': activities,
                    'user_id': str(itinerary.user_id),            
                    'username':user.username ,
                    'pictures': [picture.to_dict() for picture in itinerary.pictures]                })
            return {
                'success': True,
                'itineraries': result
            }, 200

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }, 500
        
@getitinerariesapi_blueprint.route('/<int:itinerary_id>', methods=['GET'])
class GetItinerary(Resource):
    def get(self, itinerary_id):
        # Fetch the itinerary using the itinerary_id from the URL
        itinerary = Itinerary.query.filter_by(itinerary_id=itinerary_id).first()

        if not itinerary:
            return {'message': 'Itinerary not found'}, 404

        # Serialize itinerary data
        itinerary_data = {
            'itinerary_id': str(itinerary.itinerary_id),
            'itinerary_name': itinerary.itinerary_name,
            'description': itinerary.description,
            'start_date': str(itinerary.start_date),
            'end_date': str(itinerary.end_date),
            'duration': str(itinerary.duration),
            'estimated_cost': float(itinerary.estimated_cost) if itinerary.estimated_cost is not None else None,
            'destinations': [destination.to_dict() for destination in itinerary.destinations],  # Use to_dict() for serialization
            'activities': [activity.to_dict() for activity in itinerary.activities],  # Make sure Activity model has a similar to_dict method
            'accommodations': [accommodation.to_dict() for accommodation in itinerary.accommodations],  # Make sure Accommodation model has a similar to_dict method
            'pictures': [picture.filename for picture in itinerary.pictures]  
        
        }
        
        return itinerary_data, 200
    
@itineraries_blueprint.route('', methods=['GET'])
class UserItineraries(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        print(f"Received user_id: '{user_id}'")  # Debug log

        if not user_id:
            return {"error": "User ID is required"}, 400

        # Strip whitespace
        user_id = user_id.strip()
        print(f"Stripped user_id: '{user_id}'")  # Debug log

        # Validate the UUID format for user_id
        try:
            user_id = uuid.UUID(user_id)
        except ValueError as e:
            print(f"Error converting user_id to UUID: {e}")  # Print the exception message
            return {"error": "Invalid User ID format"}, 400

        # Continue with your query...


        # Query the Itinerary model to find itineraries for the specified user
        itineraries = Itinerary.query.filter_by(user_id=user_id).all()

        # If no itineraries found, return an error message
        if not itineraries:
            return {"error": "No itineraries found for this user"}, 404

        # Serialize itinerary data for the response
        itineraries_data = [{
            "itinerary_id": str(itinerary.itinerary_id),
            "name": itinerary.itinerary_name,
            "description": itinerary.description,
            "start_date": str(itinerary.start_date),
            "end_date": str(itinerary.end_date),
            "duration": str(itinerary.duration),
            'estimated_cost': float(itinerary.estimated_cost) if itinerary.estimated_cost is not None else None,
            "destinations": [destination.to_dict() for destination in itinerary.destinations],
            "activities": [activity.to_dict() for activity in itinerary.activities],
            "accommodations": [accommodation.to_dict() for accommodation in itinerary.accommodations],
            "pictures": [picture.filename for picture in itinerary.pictures]  
        } for itinerary in itineraries]

        return itineraries_data, 200
