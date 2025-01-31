from flask_restx import Namespace

class UserPreferencesDto:
    postuserpreferencesapi = Namespace('userpreferences', description='api for user prefeences')