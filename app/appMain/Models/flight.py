from app.appMain import db

class Flight(db.Model):
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.itinerary_id'), nullable=False)
    departure_city = db.Column(db.String(255), nullable=False)
    arrival_city = db.Column(db.String(255), nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    airline = db.Column(db.String(255))
    flight_number = db.Column(db.String(255))
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'flight_id': self.flight_id,
            'departure_city': self.departure_city,
            'arrival_city': self.arrival_city,
            'departure_date': str(self.departure_date.strftime('%Y-%m-%d')),
            'arrival_date': str(self.arrival_date.strftime('%Y-%m-%d')),
            'airline': self.airline,
            'flight_number': self.flight_number,
            'notes': self.notes
        }