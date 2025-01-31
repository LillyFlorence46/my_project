from flask_restx import Resource
from flask import request
from app.appMain import db
from app.appMain.Models.chat_room import ChatRoom
from app.appMain.dto.chat_room import ChatRoomDto
from datetime import datetime
import uuid

chatroom_api_blueprint = ChatRoomDto.chatroomapi

@chatroom_api_blueprint.route('', methods=['POST'])
class CreateChatRoom(Resource):
    @chatroom_api_blueprint.expect(ChatRoomDto.chat_room)
    def post(self):
        data = request.get_json()

        # Generate room_id if not provided
        room_id = data.get('room_id') or str(uuid.uuid4())  # Generate a new UUID if not provided
        created_at = datetime.utcnow()  # Set the creation timestamp

        # Validate room_id format if provided
        if not is_valid_uuid(room_id):
            return {'message': 'Invalid room_id format'}, 400

        new_room = ChatRoom(
            room_id=room_id,
            created_at=created_at
        )

        db.session.add(new_room)
        db.session.commit()

        return {'message': 'Chat room created successfully', 'room_id': room_id}, 201

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test
