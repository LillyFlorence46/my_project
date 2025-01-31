from app.appMain import db

class Activity(db.Model):
    __tablename__ = 'activities'
    activity_id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.itinerary_id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.destination_id'), nullable=False)
    activity_name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'activity_name': self.activity_name,
            'date': str(self.date.strftime('%Y-%m-%d')),
            'time': str(self.time),
            'notes': self.notes
        }

