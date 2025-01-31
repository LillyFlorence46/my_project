from flask_restx import Resource
from flask import request,make_response
from app.appMain.Models.users import Users
from app.appMain.dto.users import AdminUsersDto
from app.appMain import db
from uuid import uuid4
import os
from flask import request
from werkzeug.utils import secure_filename
from app.appMain.dto.users import UserDto
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token 
from datetime import timedelta

signupuserapi_blueprint = UserDto.signupapi
loginuserapi_blueprint = UserDto.loginapi
updateuserdetailsapi_blueprint = UserDto.updatedetailsapi
deleteusersapi_blueprint = UserDto.deleteapi
registerdetailsapi_blueprint = AdminUsersDto.registerapi
userdetails_blueprint = UserDto.detailsapi


UPLOAD_FOLDER = '/home/lilly/Travelmate/Demo/src/assets'  # Update this path as needed
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@signupuserapi_blueprint.route('', methods=['POST'])
class Signup(Resource):
    def post(self):
        # Check if it's form data or JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        # Validate data presence
        if not data:
            return {'message': 'Request body is required'}, 400

        # Check if all required fields are present
        required_fields = ['username', 'email', 'first_name', 'last_name', 'password']
        for field in required_fields:
            if field not in data:
                return {'message': f'{field} is required'}, 400

        # Check if user already exists
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'User already exists'}, 404

        # Handle profile_pic upload
        profile_pic = None
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                profile_pic = filename
            else:
                return {'message': 'Invalid file type for profile_pic'}, 400

        # Create a new user
        new_user = Users(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            profile_pic=profile_pic  # Store only the file name
        )

        # Hash the password before saving it
        
        new_user.user_password = generate_password_hash(data['password'])

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

@loginuserapi_blueprint.route('', methods=['POST'])
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email:
            return {'message': 'Required email'}, 400

        if not password:
            return {'message': 'Required password'}, 400

        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.user_password, password):  # Compare hashed passwords
                # Proceed with generating access token
                access_token = create_access_token(
                    identity={'user_id': user.user_id, 'email': user.email},
                    expires_delta=timedelta(hours=1)
                )
                return {
                    'message': 'Login successful',
                    'access_token': access_token,
                    'username': user.username,
                    'user_id': str(user.user_id)
                }, 200
            else:
                return {'message': 'Password incorrect'}, 401
        else:
            return {'message': 'Invalid email'}, 404


# Update User Details
# @updateuserdetailsapi_blueprint.route('', methods=['PUT'])
# class UpdateUser(Resource):
#     def put(self):
#         data = request.get_json()
#         email = data.get('email')
        
#         if not email:
#             return {'message': 'Email is required'}, 400
        
#         user = Users.query.filter_by(email=email).first()
        
#         if not user:
#             return {'message': 'User not found'}, 404
        
#         # Update user details
#         user.user_name = data.get('user_name', user.user_name)
#         user.first_name = data.get('first_name', user.first_name)
#         user.last_name = data.get('last_name', user.last_name)

#         # Update password if provided
#         new_password = data.get('password')
#         if new_password:
#             user.set_password(new_password)  # Ensure you hash the password

#         db.session.commit()
#         return {'message': 'User details updated successfully'}, 200

UPLOAD_FOLDER = '/home/lilly/Travelmate/Demo/src/static/profile_pics'

@updateuserdetailsapi_blueprint.route('', methods=['PUT'])
class UpdateUser(Resource):
    def put(self):
        data = request.get_json()

        email = data.get('email')
        username = data.get('username')
        
        if not email:
            return {'message': 'Email is required'}, 400
        
        # Query the user by email
        user = Users.query.filter_by(email=email).first()
        
        if not user:
            return {'message': 'User not found'}, 404
        
        # Update the user's details with provided data
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.profile_pic  = data.get('profile_pic', user.profile_pic)

        # Update the password if provided in the request
        new_password = data.get('password')
        if new_password:
            user.set_password(new_password)  # Ensure the password is hashed

        # Commit the changes to the database
        db.session.commit()
        
        return {'message': 'User details updated successfully'}, 200


# Delete User
@deleteusersapi_blueprint.route('', methods=['DELETE'])
class DeleteUser(Resource):
    def delete(self):
        email = request.args.get('email')

        if not email:
            return {'message': 'Email is required'}, 400
        
        user = Users.query.filter_by(email=email).first()
        
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

@registerdetailsapi_blueprint.route('', methods=['GET'])
class AdminUsers(Resource):
    def get(self):

        users = Users.query.all()
        user_list = [
            {
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,

            }
            for user in users
        ]

        return make_response(user_list,200)

@userdetails_blueprint.route('', methods=['GET'])
class GetUser(Resource):
    def get(self):
        user_id = request.args.get('user_id', '').strip()
        if not user_id:
            return {"error": "User ID parameter is required"}, 400

        # Query the user by user_id
        try:
            user = Users.query.filter_by(user_id=user_id).first()
        except Exception as e:
            return {"error": f"Database query failed: {str(e)}"}, 500

        if user:
            user_data = {
                "userId": str(user.user_id),
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
            return user_data, 200  # Returning user data as a plain dictionary
        else:
            return {"error": "User not found"}, 404
        
# @listusers_blueprint.route('', methods=['GET'])
# class AdminUsers(Resource):
#     def get(self):
#         users = Users.query.all()
#         user_list = [
#             {
#                 'username': user.username,
#                 'email': user.email,
#                 'phone_number': user.phone_number,
#                 'created_at': user.created_at
#             }
#             for user in users
#         ]
 
        # return make_response(user_list,200)
 
 