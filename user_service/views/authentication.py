from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, decode_token
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

#todo: DO WE NEED TO ADD A SEESION
class RegisterResource(Resource):
    def post(self):
        try:
            data = USER_SCHEMA.load(request.json)
        except:
            return status.HTTP_400_BAD_REQUEST
        try:
            is_exists = db.session.query(User.id).filter_by(user_name=data['user_name']).scalar() is not None
            if not is_exists:
                try:
                    data['user_password'] = bcrypt.generate_password_hash(data['user_password'],round(10))
                    new_user = User(**data)
                    try:
                        db.session.add(new_user)
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                except ValueError:
                    return status.HTTP_400_BAD_REQUEST
            else:
                return status.HTTP_409_CONFLICT
        except:
            return status.HTTP_400_BAD_REQUEST
        return status.HTTP_200_OK

#todo: What about authificated user
class LoginResource(Resource):
    def post(self):
            try:
                data = USER_SCHEMA.load(request.json)
                current_user = User.find_by_user_name(data['user_name'])
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

api.add_resource(ProfileResource, '/profile')
api.add_resource(LoginResource, '/login')
api.add_resource(RegisterResource, '/register')

