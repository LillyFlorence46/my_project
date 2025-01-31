from flask import Blueprint, request
from flask_restx import Resource
from app.appMain import db
from app.appMain.Models.user_preferences import UserPreferences
from app.appMain.dto.user_preferences import UserPreferencesDto
from app.appMain.Models.users import Users

userpreferencesapi_blueprint = UserPreferencesDto.postuserpreferencesapi

@userpreferencesapi_blueprint.route('', methods=['POST', 'GET'])
class UserPreference(Resource):
    def post(self):
        try:
            data = request.get_json()

            user_id = data.get('userId')
            destinations = data.get('destinations', {})
            activities = data.get('activities', {})
            past_trips = data.get('pastTrips', {})
            favorite_travel_mode = data.get('favoriteTravelMode', {})

            # Validate user_id
            if not user_id:
                return {"error": "userId is required"}, 400

            # Check if the user_preferences entry already exists
            existing_preferences = UserPreferences.query.filter_by(user_id=user_id).first()
            if existing_preferences:
                return {"error": "Preferences for this user already exist"}, 400

            new_preferences = UserPreferences(
                user_id=str(user_id),
                destinations=destinations,
                activities=activities,
                past_trips=past_trips,
                favorite_travel_mode=favorite_travel_mode
            )

            db.session.add(new_preferences)
            db.session.commit()

            return {
                "message": "User preferences created successfully",
                "data": new_preferences.to_dict()
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def get(self):
            try:
                # Get user_id from query parameters
                user_id = request.args.get('userId')

                # Validate user_id
                if not user_id:
                    return {"error": "userId is required"}, 400

                # Fetch the user preferences based on user_id
                user_preferences = UserPreferences.query.filter_by(user_id=user_id).first()

                if not user_preferences:
                    return {"error": "User preferences not found"}, 404

                return {
                    "message": "User preferences retrieved successfully",
                    "data": user_preferences.to_dict()
                }, 200

            except Exception as e:
                return {"error": str(e)}, 500

@userpreferencesapi_blueprint.route('', methods=['PUT'])
class UpdateUserPreferences(Resource):
    def put(self):
        data = request.get_json()

        # Get the user's email and user preferences data
        email = data.get('email')
        user_id = data.get('userId')
        if not email and not user_id:
            return {'message': 'Email or UserId is required'}, 400

        # Get user_id based on email if user_id is not provided
        if not user_id:
            user = Users.query.filter_by(email=email).first()
            if not user:
                return {'message': 'User not found'}, 404
            user_id = user.user_id

        # Fetch existing user preferences
        existing_preferences = UserPreferences.query.filter_by(user_id=user_id).first()
        if not existing_preferences:
            return {'message': 'Preferences for this user not found'}, 404

        # Update preferences fields
        destinations = data.get('destinations', existing_preferences.destinations)
        activities = data.get('activities', existing_preferences.activities)
        past_trips = data.get('pastTrips', existing_preferences.past_trips)
        favorite_travel_mode = data.get('favoriteTravelMode', existing_preferences.favorite_travel_mode)

        existing_preferences.destinations = destinations
        existing_preferences.activities = activities
        existing_preferences.past_trips = past_trips
        existing_preferences.favorite_travel_mode = favorite_travel_mode
        existing_preferences.updated_at = db.func.now()

        try:
            # Commit the updated preferences to the database
            db.session.commit()
            return {'message': 'User preferences updated successfully', 'data': existing_preferences.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to update user preferences', 'error': str(e)}, 500
