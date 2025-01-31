from flask_restx import Resource
from flask import request,jsonify,Response
from app.appMain.Models.users import Users
from app.appMain.Models.accommodation import Accommodation
from app.appMain.dto.accommodations import AccommodationDto
from app.appMain import db
from app.appMain.Models.wishlist import Wishlist
from datetime import datetime

getallaccommodations_blueprint = AccommodationDto.getallaccommodationsapi

@getallaccommodations_blueprint.route('', methods=['GET'])
class GetAccommodations(Resource):
    def get(self):
        try:
            accommodations = Accommodation.query.all()
            if not accommodations:
                return {"message": "No accommodations found"}, 404
            
            accommodations_list = []
            for accommodation in accommodations:
                accommodations_list.append({
                    'accommodation_id': accommodation.accommodation_id,  # Access the accommodation object's ID
                    'itinerary_id': accommodation.itinerary_id,
                    'hotel_name': accommodation.hotel_name,              # Access the accommodation object's name
                    'address': accommodation.address,                      # Access the accommodation object's address
                    'notes': accommodation.notes
                })

            return {"accommodations": accommodations_list}, 200
        except Exception as e:
            return {"error": str(e)}, 500