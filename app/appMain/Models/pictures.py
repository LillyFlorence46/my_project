from app.appMain import db
import uuid

class Picture(db.Model):
    __tablename__ = 'pictures'
    
    picture_id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.itinerary_id'), nullable=False)

    def to_dict(self):
        return {
            'picture_id': self.picture_id, 
            'filename': self.filename,
            'itinerary_id': self.itinerary_id
        }
