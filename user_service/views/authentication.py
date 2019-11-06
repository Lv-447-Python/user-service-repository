from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, decode_token
from sqlalchemy.orm.exc import UnmappedInstanceError

from user_service import db
from user_service import api
from user_service.models.user import User
from user_service.serializers.user_schema import UserSchema
from flask import jsonify, request, session, make_response
from flask_restful import Resource
from user_service import bcrypt
from flask_api import status
from marshmallow import ValidationError


USER_SCHEMA = UserSchema()

JWT_TOKEN = 'jwt_token'


class ProfileResource(Resource):
    """Implementation profile methods for editing user data"""
    def get(self):
        try:
            access = session[JWT_TOKEN]
        except IndentationError:
            return status.HTTP_401_UNAUTHORIZED
        try:
            user_info = decode_token(access)
            user_name = user_info['identity']
            current_user = User.find_by_user_name(user_name)
            try:
                user_to_response = USER_SCHEMA.dump(current_user)
                return make_response(jsonify(user_to_response),status.HTTP_200_OK)
            except KeyError:
                return status.HTTP_401_UNAUTHORIZED
        except ValueError:
            return status.HTTP_400_BAD_REQUEST

    def put(self):
        try:
            new_user = USER_SCHEMA.load(request.json)
        except ValidationError:
            return status.HTTP_400_BAD_REQUEST
        try:
            access = session[JWT_TOKEN]
            user_info = decode_token(access)
            user_name = user_info['identity']
            try:
                current_user = User.find_by_user_name(user_name)
                current_user.user_email = new_user['user_email']
                current_user.user_password = bcrypt.generate_password_hash(new_user['user_password'])
                current_user.user_first_name = new_user['user_first_name']
                current_user.user_last_name = new_user['user_last_name']
                current_user.user_image_file = new_user['user_image_file']
                try:
                    db.session.commit()
                    return status.HTTP_200_OK
                except IntegrityError:
                    db.session.rollback()
                    return status.HTTP_400_BAD_REQUEST
            except ValueError:
                return status.HTTP_400_BAD_REQUEST
        except IndentationError:
            return status.HTTP_401_UNAUTHORIZED


#TODO: IF ONLY BUTTON DELETE CHANGE METHOD TO POST
class DeleteResource(Resource):
    """Implementation of method delete user account"""
    def get(self):
        try:
            access = session[JWT_TOKEN]
        except IndentationError:
            return status.HTTP_401_UNAUTHORIZED
        try:
            user_info = decode_token(access)
            user_name = user_info['identity']
            current_user = User.find_by_user_name(user_name)
            try:
                db.session.delete(current_user)
                db.session.commit()
                session.clear()
                return status.HTTP_200_OK
            except IntegrityError:
                db.session.rollback()
                return status.HTTP_400_BAD_REQUEST
        except UnmappedInstanceError:
            return status.HTTP_400_BAD_REQUEST


api.add_resource(ProfileResource, '/profile')
api.add_resource(DeleteResource, '/delete')