from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required,create_access_token
 
db = SQLAlchemy()
ma = Marshmallow()
 
def mydb():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'travelmate'  # Change this to a secret key
    jwt = JWTManager(app)  # Initialize the JWTManager with the app

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = '/home/lilly/Travelmate/Demo/src/static/profile_pics'
    db.init_app(app)
    ma.init_app(app)
    return app

 