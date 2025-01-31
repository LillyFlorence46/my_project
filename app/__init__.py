from flask import Blueprint
from flask_restx import Api
from app.appMain.controllers.users import (signupuserapi_blueprint,
            loginuserapi_blueprint,
            deleteusersapi_blueprint,
            updateuserdetailsapi_blueprint,
            registerdetailsapi_blueprint,
            userdetails_blueprint)
from app.appMain.controllers.itineraries import (createtitineraryapi_blueprint,
            getitinerariesapi_blueprint,
            updateitinerariesapi_blueprint,
            deleteitinerariesapi_blueprint,
            getallitinerariesapi_blueprint,
            itineraries_blueprint,
            wishlistapi_blueprint)
from app.appMain.controllers.chat import (sendmessageapi_blueprint)
from app.appMain.controllers.chat_room import (chatroom_api_blueprint )
from app.appMain.controllers.activities import(getallactivities_blueprint)
from app.appMain.controllers.accommodations import (getallaccommodations_blueprint)
from app.appMain.controllers.user_preferences import(userpreferencesapi_blueprint)
blueprint = Blueprint('api',__name__)
api = Api(blueprint, title='travelmate')

api.add_namespace(signupuserapi_blueprint)
api.add_namespace(loginuserapi_blueprint)
api.add_namespace(deleteusersapi_blueprint)
api.add_namespace(updateuserdetailsapi_blueprint)
api.add_namespace(registerdetailsapi_blueprint)
api.add_namespace(userdetails_blueprint)

api.add_namespace(createtitineraryapi_blueprint)
api.add_namespace(getitinerariesapi_blueprint)
api.add_namespace(updateitinerariesapi_blueprint)
api.add_namespace(deleteitinerariesapi_blueprint)
api.add_namespace(getallitinerariesapi_blueprint)
api.add_namespace(itineraries_blueprint)
api.add_namespace(wishlistapi_blueprint)

api.add_namespace(sendmessageapi_blueprint)

api.add_namespace(chatroom_api_blueprint )

api.add_namespace(getallactivities_blueprint)


api.add_namespace(getallaccommodations_blueprint)

api.add_namespace(userpreferencesapi_blueprint)