from flask_restx import Namespace

class ActivityDto:
    getallactivitiesapi = Namespace('getactivities', description='api to create activity')
    