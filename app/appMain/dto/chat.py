from flask_restx import Namespace, fields

class ChatDto:
    sendmessageapi = Namespace('send_message', description='API for user chat')

    chat_message = sendmessageapi.model('ChatMessage', {
        'sender_id': fields.String(required=True, description='The ID of the sender (UUID)'),
        'room_id': fields.String(required=True, description='The ID of the chat room (UUID)'),
        'content': fields.String(required=True, description='The message content')
    })
