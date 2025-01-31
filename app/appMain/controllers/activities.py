from flask_restx import Resource
from flask import request,jsonify,Response
from app.appMain.Models.users import Users
from app.appMain.Models.activity import Activity
from app.appMain.dto.activities import ActivityDto
from app.appMain import db
from app.appMain.Models.wishlist import Wishlist
from datetime import datetime

getallactivities_blueprint = ActivityDto.getallactivitiesapi

@getallactivities_blueprint.route('', methods=['GET'])
class GetActivities(Resource):
    def get(self):
        try:
            # Fetch all activities
            activities = Activity.query.all()  # Retrieve all activities

            if not activities:
                return {"message": "No activities found"}, 404

            # Format the activities into a list of dictionaries to return as JSON
            activities_list = []
            for activity in activities:
                activities_list.append({
                    'activity_id': activity.activity_id,  # Access the activity object's ID
                    'itinerary_id': activity.itinerary_id,
                    'name': activity.activity_name,        # Access the activity object's name
                    'description': activity.notes,  # Access the activity object's description
                    'date': activity.date.strftime('%Y-%m-%d') if activity.date else None  # Access the activity object's date
                })

            return {"activities": activities_list}, 200

        except Exception as e:
            return {"error": str(e)}, 500
