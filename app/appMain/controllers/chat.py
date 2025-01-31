from flask_restx import Resource
from flask import request
from app.appMain import db
from app.appMain.Models.chat import ChatMessage
from app.appMain.Models.users import Users
from app.appMain.dto.chat import ChatDto
import uuid

# Create blueprints for chat-related APIs
sendmessageapi_blueprint = ChatDto.sendmessageapi

# API to send a chat message
@sendmessageapi_blueprint.route('', methods=['POST'])
class SendMessage(Resource):
    def post(self):
        data = request.get_json()
        
        # Extract required fields
        sender_id = data.get('sender_id')
        room_id = data.get('room_id')
        content = data.get('content')

        if not all([sender_id, room_id, content]):
            return {'message': 'Missing required fields'}, 400

        # Check if the sender exists
        user = Users.query.filter_by(user_id=sender_id).first()
        if not user:
            return {'message': 'Sender not found'}, 404

        # Validate room_id format
        try:
            uuid.UUID(room_id)  # Validate UUID
        except ValueError:
            return {'message': 'Invalid room_id format'}, 400

        # Create a new chat message instance
        new_message = ChatMessage(
            sender_id=sender_id,
            room_id=room_id,
            content=content
        )

        # Save the new message in the database
        try:
            db.session.add(new_message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': 'Failed to send message', 'error': str(e)}, 500

        return {'message': 'Message sent successfully', 'message_id': new_message.message_id}, 201
