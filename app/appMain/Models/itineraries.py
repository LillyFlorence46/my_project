from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime




class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    itinerary_id = db.Column(db.Integer, primary_key=True)  
    itinerary_name= db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)  
    estimated_cost = db.Column(db.Numeric(10, 2), nullable=False)  # New column added
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)  
    
    users = db.relationship('Users', backref='itineraries', lazy=True)  # Add this line
    destinations = db.relationship('Destination', backref='itinerary', lazy=True)
    flights = db.relationship('Flight', backref='itinerary', lazy=True)
    accommodations = db.relationship('Accommodation', backref='itinerary', lazy=True)
    activities = db.relationship('Activity', backref='itinerary', lazy=True)
    pictures = db.relationship('Picture', backref='itinerary', lazy=True)

    def to_dict(self):
        return {
            'itinerary_id': self.itinerary_id,
            'user_id': str(self.user_id),
            'itinerary_name': self.itinerary_name,
            'description': self.description,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,     
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'duration': self.duration,
            'estimated_cost': float(self.estimated_cost) if self.estimated_cost is not None else None,
            'destinations': [dest.to_dict() for dest in self.destinations],
            'accommodations': [accommodation.to_dict() for accommodation in self.accommodations],
            'activities': [activity.to_dict() for activity in self.activities]
        }


def __init__(self, **kwargs):
    super(Itinerary, self).__init__(**kwargs)

    
@property
def formatted_start_date(self):
    return self.start_date.strftime('%Y-%m-%d')
    
