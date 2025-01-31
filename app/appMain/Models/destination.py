from app.appMain import db

class Destination(db.Model):
    __tablename__ = 'destinations'
    destination_id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.itinerary_id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'destination_id': self.destination_id,
            'location': self.location,
            'duration': self.duration,
            'notes': self.notes
        }