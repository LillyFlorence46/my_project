from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    message_id = db.Column(db.Integer, primary_key=True)  
    sender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)  
    room_id = db.Column(UUID(as_uuid=True), nullable=False)  
    content = db.Column(db.Text, nullable=False)  
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  
    def __init__(self, sender_id, room_id, content):
        self.sender_id = sender_id
        self.room_id = room_id
        self.content = content

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'sender_id': str(self.sender_id),
            'room_id': str(self.room_id),
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None,
        }

@property
def formatted_timestamp(self):
    return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
