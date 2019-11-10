from flask_jwt_extended import create_access_token
from user_service import api
from user_service.models.user import User
from user_service.serializers.user_schema import LoginSchema
from flask import jsonify, request, session, make_response
from flask_restful import Resource
from user_service import bcrypt
from flask_api import status

LOGIN_SCHEMA = LoginSchema()

JWT_TOKEN = 'jwt_token'


# TODO: IF ONLY BUTTON LOGOUT CHANGE TO POST METHOD
class LogoutResource(Resource):
    """Implementation sign out method"""
    def get(self):
        session.clear()
        response = {'is_logout': True}
        return make_response(jsonify(response), status.HTTP_200_OK)


# TODO: Refactoring this code with change try-except and type error avoid nested try-except
class LoginResource(Resource):
    """Implementation sign in method"""
    def post(self):
            try:
                data = LOGIN_SCHEMA.load(request.json)
                current_user = User.find_user(user_name=data['user_name'])
                if bcrypt.check_password_hash(current_user.user_password,data['user_password']):
                    try:
                        session.permanent = True
                        access_token = create_access_token(identity=current_user.user_name, expires_delta=False)
                        session[JWT_TOKEN] = access_token
                        return status.HTTP_200_OK
                    except:
                        return status.HTTP_400_BAD_REQUEST
                else:
                    return status.HTTP_400_BAD_REQUEST
            except:
                return status.HTTP_400_BAD_REQUEST

api.add_resource(LogoutResource, '/logout')
api.add_resource(LoginResource, '/login')
