from app.appMain import db
from sqlalchemy.dialects.postgresql import JSONB, UUID
from datetime import datetime

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), primary_key=True, nullable=False)
    destinations = db.Column(JSONB, nullable=True, default={})  # Default as empty JSON
    activities = db.Column(JSONB, nullable=True, default={})    # Default as empty JSON
    past_trips = db.Column(JSONB, nullable=True, default={})    # Default as empty JSON
    favorite_travel_mode = db.Column(JSONB, nullable=True, default={})  # Default as empty JSON
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            "destinations": self.destinations,
            "activities": self.activities,
            "pastTrips": self.past_trips,
            "favoriteTravelMode": self.favorite_travel_mode,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }

    def __init__(self, **kwargs):
        super(UserPreferences, self).__init__(**kwargs)
