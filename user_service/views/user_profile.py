"""User profile resource view"""
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import decode_token, create_access_token
from sqlalchemy.orm import exc
from flask import jsonify, request, session, make_response
from flask_restful import Resource
from flask_api import status
from marshmallow import ValidationError
from flask_mail import Message
from user_service import DB
from user_service import API
from user_service.models.user import User
from user_service.serializers.user_schema import UserSchema, LoginSchema
from user_service import BCRYPT
from user_service.utils.user_utils import get_reset_token, verify_reset_token
from user_service import MAIL

USER_SCHEMA = UserSchema(exclude=['id', 'user_registration_data'])


JWT_TOKEN = 'jwt_token'


def send_email(user_email, token):
    """
    Implementation of sending message on email
    Args:
        user_email:
        token:

    Returns:
        status
    """
    try:
        msg = Message("Hello, you tried to reset password!", sender='testingforserve@gmail.com',
                      recipients=[user_email])
        msg.body = f'''To reset your password just follow this link: {API.url_for(ResetPasswordRequestResource, 
        token=token, _external=True)} 
        If you haven`t tried to reset your password just ignore this message'''
        MAIL.send(msg)
    except RuntimeError:
        return status.HTTP_400_BAD_REQUEST
    return status.HTTP_200_OK


class ResetPasswordRequestResource(Resource):
    """Implementation of reset password request on mail"""
    def post(self):
        """Post method for reset password"""
        try:
            data = request.json
            user_email = data['user_email']
        except ValidationError as error:
            return make_response(jsonify(error.messages), status.HTTP_400_BAD_REQUEST)
        try:
            user = User.query.filter_by(user_email=user_email).scalar()
            token = get_reset_token(user)
            try:
                send_email(user_email, token)
                return status.HTTP_200_OK
            except ValueError:
                response_object = {
                    'Error': 'No user found'
                }
                return make_response(response_object, status.HTTP_401_UNAUTHORIZED)
        except:
            return status.HTTP_400_BAD_REQUEST

    def put(self):
        """Put method for reset password"""
        try:
            token = request.args.get('token')
        except TimeoutError:
            return status.HTTP_504_GATEWAY_TIMEOUT
        try:
            user = verify_reset_token(token)
            data = request.json
            user_password = data['user_password']
            user_password_confirm = data['user_password_confirm']
        except ValidationError as error:
            return make_response(jsonify(error.messages), status.HTTP_400_BAD_REQUEST)
        try:
            if user_password == user_password_confirm:
                try:
                    user.user_password = BCRYPT.generate_password_hash(user_password, 10).decode('utf-8')
                    DB.session.commit()
                    return status.HTTP_200_OK
                except IntegrityError:
                    DB.session.rollback()
                    response_object = {
                        'Error': 'Database error'
                    }
                    return make_response(jsonify(response_object), status.HTTP_400_BAD_REQUEST)
            else:
                raise TypeError
        except TypeError:
                response_object = {
                    'Error': 'Passwords do not match'
                }
                return make_response(response_object, status.HTTP_400_BAD_REQUEST)

class ProfileResource(Resource):
    """Implementation profile methods for editing user data"""

    def post(self):
        """Post method for creating an user"""
        try:
            new_user = USER_SCHEMA.load(request.json)
        except ValidationError as error:
            return make_response(jsonify(error.messages),
                                 status.HTTP_400_BAD_REQUEST)
        try:
            is_exists = DB.session.query(User.id).filter_by(user_name=new_user.user_name).scalar() is not None
            if not is_exists:
                try:
                    new_user.user_password = BCRYPT.generate_password_hash(new_user.user_password, round(10)).decode(
                        'utf-8')
                except ValidationError as error:
                    return make_response(jsonify(error.messages), status.HTTP_400_BAD_REQUEST)
            else:
                raise ValueError
        except ValueError:
            response_object = {
                'Error': 'This user already exists'
            }
            return make_response(response_object, status.HTTP_409_CONFLICT)
        try:
            DB.session.add(new_user)
            DB.session.commit()
            session.permanent = True
            access_token = create_access_token(identity=new_user.id, expires_delta=False)
            session[JWT_TOKEN] = access_token
            return status.HTTP_200_OK
        except IntegrityError:
            DB.session.rollback()
            response_object = {
                'Error': 'Database error'
            }
            return make_response(jsonify(response_object), status.HTTP_400_BAD_REQUEST)

    def get(self):
        """Get method for returning user data"""
        try:
            access = session[JWT_TOKEN]
        except KeyError:
            response_object = {
                'Error': 'You`re unauthorized'
            }
            return make_response(response_object, status.HTTP_401_UNAUTHORIZED)
        try:
            user_info = decode_token(access)
            user_id = user_info['identity']
            current_user = User.find_user(id=user_id)
            if current_user is not None:
                try:
                    user_to_response = USER_SCHEMA.dump(current_user)
                    return make_response(jsonify(user_to_response), status.HTTP_200_OK)
                except ValidationError as error:
                    return make_response(jsonify(error.messages), status.HTTP_400_BAD_REQUEST)
            else:
                raise ValueError
        except ValueError:
            response_object = {
                'Error': "This user doesn`t exists"
            }
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)

    def put(self):
        """Put metod for editing user data"""
        try:
            new_user = USER_SCHEMA.load(request.json)
        except ValidationError as error:
            return make_response(jsonify(error.messages), status.HTTP_400_BAD_REQUEST)
        try:
            access = session[JWT_TOKEN]
            user_info = decode_token(access)
            user_id = user_info['identity']
        except KeyError:
            response_object = {
                'Error': 'Session has been expired'
            }
            return make_response(response_object, status.HTTP_401_UNAUTHORIZED)
        try:
            current_user = User.find_user(id=user_id)
            if current_user is not None:
                current_user.user_email = new_user.user_email
                current_user.user_password = BCRYPT.generate_password_hash(new_user.user_password).decode(
                    'utf-8')
                current_user.user_first_name = new_user.user_first_name
                current_user.user_last_name = new_user.user_last_name
                current_user.user_image_file = new_user.user_image_file
            else:
                raise ValueError
        except ValueError:
            response_object = {
                'Error': 'This user doesn`t exists'
            }
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)
        try:
            DB.session.commit()
            return status.HTTP_200_OK
        except IntegrityError:
            DB.session.rollback()
            response_object = {
                'Error': 'Database error'
            }
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)

    def delete(self):
        """Delete method for deleting user account"""
        try:
            access = session[JWT_TOKEN]
        except KeyError:
            response_object = {
                'Error': 'You`re unauthorized'
            }
            return make_response(response_object, status.HTTP_401_UNAUTHORIZED)
        try:
            user_info = decode_token(access)
            user_id = user_info['identity']
            current_user = User.find_user(id=user_id)
            DB.session.delete(current_user)
        except exc.UnmappedInstanceError:
            response_object = {
                'Error': 'This user doesn`t exists'
            }
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)
        try:
            DB.session.commit()
            session.clear()
            return status.HTTP_200_OK
        except IntegrityError:
            response_object = {
                'Error': 'Database error'
            }
            DB.session.rollback()
            return make_response(response_object, status.HTTP_400_BAD_REQUEST)


API.add_resource(ProfileResource, '/profile')
API.add_resource(ResetPasswordRequestResource, '/reset-password')
