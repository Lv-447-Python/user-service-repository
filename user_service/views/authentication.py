from user_service import app
from user_service import db
from user_service import api
from user_service.models.user import User
from user_service.serializers.user_schema import UserSchema
from flask import jsonify
from flask_restful import Resource

USER_SCHEMA = UserSchema()


class HelloWorld(Resource):
    def get(self):
        exists = db.session.query(User.id).filter_by(user_name='Petro').scalar() is not None
        print(exists)
        if not exists:
            new_user = User(user_name="Petro",
                            user_email="www-",
                            user_password="pass",
                            user_first_name="Nazar",
                            user_last_name="Hrytsiv",
                            user_image_file="path")
            db.session.add(new_user)
            db.session.commit()
            return "Created"
        else:
            user = User.query.first()
            user_serialize = USER_SCHEMA.dump(user)
            return jsonify(user_serialize)

api.add_resource(HelloWorld, '/main')
