from flask_restx import Namespace

class ItineraryDto:
    createitineraryapi = Namespace('createitinerary',description='api to create itinerary')
    getitinerariesapi = Namespace('getitineraries', description='api to get itineraies')
    updateitinerariesapi = Namespace('updateitineraries', description='api tp update itineraries')
    deleteitinerariesapi = Namespace('deleteitineraries', description='api to delete itineraries')
    getallitinerariesapi = Namespace('getallitineraries', description='api to get all itineraries')
    itinerariesapi = Namespace('itineraries', description='api to get user itineraries')
    wishlistitinerariesapi = Namespace('wishlist', description='api to wishlist itineraries')
