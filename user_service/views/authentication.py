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
from user_service.configs.logger import logger


LOGIN_SCHEMA = LoginSchema()

JWT_TOKEN = 'jwt_token'


# TODO: IF ONLY BUTTON LOGOUT CHANGE TO POST METHOD
class LogoutResource(Resource):
    """
    Implementation sign out method
    """
    def get(self):
        """
        Get method for signing out
        Args:
            self
        Returns:
            status
        """
        session.clear()
        response = {
            'is_logout': True,
        }
        logger.info("Successful request to LogoutResource, method GET")
        return make_response(response, status.HTTP_200_OK)


class LoginResource(Resource):
    """Implementation sign in method"""
    def post(self):
        """
        Post method for signing in
        Args:
            self
        Returns:
            status
        """
        try:
            data = LOGIN_SCHEMA.load(request.json)
            current_user = User.find_user(user_name=data['user_name'])
        except ValidationError as error:
            logger.error("Invalid data for login")
            return make_response(jsonify(error.messages), status.HTTP_400_BAD_REQUEST)
        except KeyError as error:
            logger.error("Missing data")
            response_object = {
                'Error': 'You didn`t enter required data'
            }
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)
        check_password = BCRYPT.check_password_hash(current_user.user_password, data['user_password'])
        if not check_password:
            response_object = {
                'Error': 'Your password or login is invalid'
            }
            logger.error("Invalid login or password")
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)
        session.permanent = True
        access_token = create_access_token(identity=current_user.id, expires_delta=False)
        session[JWT_TOKEN] = access_token
        logger.info("Successful request to LoginResource, method POST")
        return status.HTTP_200_OK

class AuthResource(Resource):
    """Implementation sign in method"""
    def get(self):
        try:
            session[JWT_TOKEN]
            return status.HTTP_200_OK
        except:
            return status.HTTP_400_BAD_REQUEST


API.add_resource(LogoutResource, '/logout')
API.add_resource(LoginResource, '/login')
API.add_resource(AuthResource, '/auth')
