from app.appMain import db

class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    wishlist_id = db.Column(db.Integer, primary_key=True)
    itinerary_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, db.ForeignKey('users.email'), nullable=False)  # Foreign key referencing the Users table    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.itinerary_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

