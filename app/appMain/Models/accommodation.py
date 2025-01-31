from app.appMain import db



class Accommodation(db.Model):
    __tablename__ = 'accommodations'
    accommodation_id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.itinerary_id'), nullable=False)
    hotel_name = db.Column(db.String(255), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255))
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'accommodation_id': self.accommodation_id,
            'hotel_name': self.hotel_name,
            'check_in_date': str(self.check_in_date.strftime('%Y-%m-%d')),
            'check_out_date': str(self.check_out_date.strftime('%Y-%m-%d')),
            'address': self.address,
            'notes': self.notes
        }

