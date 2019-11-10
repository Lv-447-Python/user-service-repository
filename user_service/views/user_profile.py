from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import UnmappedInstanceError
from user_service import db
from user_service import api
from user_service.models.user import User
from user_service.serializers.user_schema import UserSchema, LoginSchema
from flask import jsonify, request, session, make_response
from flask_restful import Resource
from user_service import bcrypt
from flask_api import status
from marshmallow import ValidationError
from user_service.utils.user_utils import get_reset_token,verify_reset_token
from user_service import mail
from flask_mail import Message


USER_SCHEMA = UserSchema(exclude=['id','user_registration_data'])

LOGIN_SCHEMA = LoginSchema()

JWT_TOKEN = 'jwt_token'


def send_email(user_email,token):
    """
    Implementation of sending message on email
    Args:
        user_email:
        token:

    Returns:
        status
    """
    try:
        msg = Message("Hello, you tried to reset password", sender = 'testingforserve@gmail.com', recipients = [user_email])
        msg.body = f'''For reset your password just follow this link: {api.url_for(ResetPasswordRequestResource, token=token, _external=True)} 
        If you didn`t reset your password just ignore this message'''
        mail.send(msg)
    except:
        return status.HTTP_400_BAD_REQUEST
    return status.HTTP_200_OK

# TODO: Refactoring this code with change try-except and type error avoid nested try-except
class ResetPasswordRequestResource(Resource):
    """Implementation of reset password request on mail"""
    def post(self):
        try:
            data = request.json
            user_email = data['user_email']
            try:
                user = User.query.filter_by(user_email=user_email).scalar()
                token = get_reset_token(user)
                try:
                    send_email(user_email, token)
                    return status.HTTP_200_OK
                except ValueError:
                    return status.HTTP_401_UNAUTHORIZED
            except:
                return status.HTTP_405_METHOD_NOT_ALLOWED
        except:
            return status.HTTP_408_REQUEST_TIMEOUT

    def put(self):
        try:
            token = request.args.get('token')
        except:
            return status.HTTP_504_GATEWAY_TIMEOUT
        try:
            user = verify_reset_token(token)
            data = request.json
            user_password = data['user_password']
            user_password_confirm = data['user_password_confirm']
            try:
                if user_password == user_password_confirm:
                    try:
                        user.user_password = bcrypt.generate_password_hash(user_password,10).decode('utf-8')
                        db.session.commit()
                        return status.HTTP_200_OK
                    except IntegrityError:
                        db.session.rollback()
                        return status.HTTP_400_BAD_REQUEST
                else:
                    raise ValidationError
            except:
                return status.HTTP_400_BAD_REQUEST
        except:
            return status.HTTP_400_BAD_REQUEST

# TODO: Refactoring this code with change try-except and type error avoid nested try-except
class ProfileResource(Resource):
    """Implementation profile methods for editing user data"""
    def post(self):
        try:
            data = USER_SCHEMA.load(request.json)
        except:
            return status.HTTP_400_BAD_REQUEST
        try:
            is_exists = db.session.query(User.id).filter_by(user_name=data['user_name']).scalar() is not None
            if not is_exists:
                try:
                    data['user_password'] = bcrypt.generate_password_hash(data['user_password'],round(10)).decode('utf-8')
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

    def get(self):
        try:
            access = session[JWT_TOKEN]
        except KeyError:
            return status.HTTP_401_UNAUTHORIZED
        try:
            user_info = decode_token(access)
            user_name = user_info['identity']
            print(user_name)
            current_user = User.find_user(user_name = user_name)
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
                #Make an unpacking?
                current_user = User.find_user(user_name=user_name)
                current_user.user_email = new_user['user_email']
                current_user.user_password = bcrypt.generate_password_hash(new_user['user_password']).decode('utf-8')
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

    """Implementation of method delete user account"""
    def delete(self):
        try:
            access = session[JWT_TOKEN]
        except IndentationError:
            return status.HTTP_401_UNAUTHORIZED
        try:
            user_info = decode_token(access)
            user_name = user_info['identity']
            current_user = User.find_user(user_name=user_name)
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
api.add_resource(ResetPasswordRequestResource, '/reset-password')
