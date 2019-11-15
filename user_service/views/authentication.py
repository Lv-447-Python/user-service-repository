"""Authentication resource views"""
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from flask_restful import Resource
from flask_api import status
from flask import jsonify, request, session, make_response
from user_service.serializers.user_schema import LoginSchema
from user_service import API
from user_service.models.user import User
from user_service import BCRYPT

LOGIN_SCHEMA = LoginSchema()

JWT_TOKEN = 'jwt_token'


# TODO: IF ONLY BUTTON LOGOUT CHANGE TO POST METHOD
class LogoutResource(Resource):
    """
    Implementation sign out method
    """
    def get(self):
        """Get method for sign out"""
        session.clear()
        response = {
            'is_logout': True,
        }
        return make_response(response, status.HTTP_200_OK)


class LoginResource(Resource):
    """Implementation sign in method"""
    def post(self):
        """Post method for sign in"""
        try:
            data = LOGIN_SCHEMA.load(request.json)
            current_user = User.find_user(user_name=data['user_name'])
        except ValidationError as error:
            return make_response(jsonify(error.messages), status.HTTP_400_BAD_REQUEST)
        try:
            BCRYPT.check_password_hash(current_user.user_password, data['user_password'])
        except AttributeError:
            response_object = {
                'Error': 'Account not found'
            }
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)

        session.permanent = True
        access_token = create_access_token(identity=current_user.id, expires_delta=False)
        session[JWT_TOKEN] = access_token
        return status.HTTP_200_OK


API.add_resource(LogoutResource, '/logout')
API.add_resource(LoginResource, '/login')
