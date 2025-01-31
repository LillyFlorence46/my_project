from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)  # Updated column name
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "userId": self.user_id,
            "username": self.username,
            "email": self.email,
            "profilePic": self.profile_pic,
        }

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    @property
    def password(self):
        return self.user_password  # Return the hashed password

    @password.setter
    def password(self, password):
        # Use scrypt for password hashing
        self.user_password = generate_password_hash(password, method='scrypt', salt_length=16)

    def verify_password(self, password):
        # Use check_password_hash to compare the hashed password
        return check_password_hash(self.user_password, password)
