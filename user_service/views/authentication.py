from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, decode_token
from user_service import db
from user_service import api
from user_service.models.user import User
from user_service.serializers.user_schema import UserSchema
from flask import jsonify, request, session
from flask_restful import Resource
from user_service import bcrypt
from flask_api import status
from marshmallow import ValidationError


USER_SCHEMA = UserSchema()

AUTH_TOKEN_KEY = 'auth_token'

class ProfileResource(Resource):
    def get(self):
        exists = db.session.query(User.id).filter_by(user_name='Marta').scalar() is not None
        print(exists)
        if not exists:
            password = "pass"
            pw_hash = bcrypt.generate_password_hash(password,10)
            new_user = User(user_name="Marta",
                            user_email=password,
                            user_password=pw_hash,
                            user_first_name="Nazar",
                            user_last_name="Hrytsiv",
                            user_image_file="path")
            db.session.add(new_user)
            session.permanent = True
            access_token = create_access_token(identity=new_user.id, expires_delta=False)
            session[AUTH_TOKEN_KEY] = access_token
            db.session.commit()
            return "Created"
        else:
            user = User.query.filter_by(user_name='Marta').scalar()
            print(session)
            user_serialize = USER_SCHEMA.dump(user)
            return jsonify(user_serialize)

    def put(self):
        try:
            new_user = USER_SCHEMA.load(request.json)
        except ValidationError:
            return status.HTTP_400_BAD_REQUEST
        try:
            current_user = User.find_by_user_name(new_user['user_name'])
            # current_user = User(user_name=new_user['user_name'],
            #                     user_email=new_user['user_email'],
            #                     user_password=bcrypt.generate_password_hash(new_user['user_password']),
            #                     user_first_name=new_user['user_first_name'],
            #                     user_last_name=new_user['user_last_name'],
            #                     user_image_file=new_user['user_image_file'],
            #                     )

            current_user.user_email = new_user['user_email']
            current_user.user_password = bcrypt.generate_password_hash(new_user['user_password'])
            current_user.user_first_name = new_user['user_first_name']
            current_user.user_last_name = new_user['user_last_name']
            current_user.user_image_file = new_user['user_image_file']
            print(session)
            try:
                db.session.commit()
                return status.HTTP_200_OK
            except IntegrityError:
                db.session.rollback()
                return status.HTTP_400_BAD_REQUEST
        except:
            return status.HTTP_409_CONFLICT



api.add_resource(ProfileResource, '/login')
# api.add_resource(ProfileResource, '/user/profile')

