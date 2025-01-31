from flask_restx import Namespace

class UserDto:
    signupapi = Namespace('user-signup',description='api for user signup')
    loginapi = Namespace('userlogin', description='user api login')
    updatedetailsapi = Namespace('updatedetails', description='api to update user details')
    deleteapi = Namespace('deleteuser', description='api to delete user account')
    detailsapi = Namespace('getuser', description='api to get user details')

class AdminUsersDto:
    registerapi = Namespace('users', description='api to show registered users')
