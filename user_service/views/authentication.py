from user_service import db
from user_service import api
from user_service.models.user import User
from user_service.serializers.user_schema import UserSchema
from flask import jsonify, request
from flask_restful import Resource
from user_service import bcrypt
from marshmallow import ValidationError


USER_SCHEMA = UserSchema()


class ProfileResource(Resource):
    def get(self):
        exists = db.session.query(User.id).filter_by(user_name='Orest').scalar() is not None
        print(exists)
        if not exists:
            password = "pass"
            pw_hash = bcrypt.generate_password_hash(password,10)
            new_user = User(user_name="Orest",
                            user_email=password,
                            user_password=pw_hash,
                            user_first_name="Nazar",
                            user_last_name="Hrytsiv",
                            user_image_file="path")
            db.session.add(new_user)
            db.session.commit()
            return "Created"
        else:
            user = User.query.filter_by(user_name='Orest').scalar()
            user_serialize = USER_SCHEMA.dump(user)
            return jsonify(user_serialize)

    def post(self):
        try:
            new_user = USER_SCHEMA.load(request.json)
        except:
            raise ValidationError
        try:
            current_user = User.find_by_user_name(new_user['user_name'])
            print(current_user.user_name)
        except:
            return "This user doesn`t exist"



api.add_resource(ProfileResource, '/login')
# api.add_resource(ProfileResource, '/user/profile')

