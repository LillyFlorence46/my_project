from flask_restx import Namespace, fields

class ChatRoomDto:
    chatroomapi = Namespace('chatroom', description='API for chat room management')
    
    chat_room = chatroomapi.model('ChatRoom', {
        'room_id': fields.String(required=True, description='The unique identifier for the chat room'),
        'created_at': fields.DateTime(description='Timestamp when the chat room was created')
    })
