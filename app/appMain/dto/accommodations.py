from flask_restx import Namespace

class AccommodationDto:
    getallaccommodationsapi = Namespace('getaccommodations', description='api to view accommodations')
    