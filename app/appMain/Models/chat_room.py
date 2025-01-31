from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'

    room_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
