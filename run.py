from user_service import app
from user_service import api
from user_service import db
from user_service.models.user import User
from user_service.serializers.user_schema import UserSchema
from flask import jsonify

USER_SCHEMA = UserSchema()

@app.route('/')
def index():
    exists = db.session.query(User.id).filter_by(user_name='Coffemol').scalar() is not None
    print(exists)
    if not exists:
        new_user = User(user_name="Coffemol",
                        user_email="qqqq",
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

    
if __name__ == '__main__':
    app.run()
