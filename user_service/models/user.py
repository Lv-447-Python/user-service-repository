"""Model for user-service"""
from user_service import db
from flask_security import UserMixin
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from user_service import app


class User(db.Model, UserMixin):
    """ Represent database table user by class
    :param: integer id for user
    :param: string name for user
    :param: string email for user
    :param: string password for user
    :param: string first name for user
    :param: string last name for user
    :param: string path to user image file
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), nullable=False, unique=True)
    user_email = db.Column(db.String(35), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_first_name = db.Column(db.String(25), nullable=False)
    user_last_name = db.Column(db.String(25), nullable=False)
    user_image_file = db.Column(db.String(25), nullable=False)
    user_registration_data = db.Column(db.DateTime(), nullable=False,
                                       default=datetime.datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
#kwargs
    @classmethod
    def find_by_user_name(cls,user_name):
        return cls.query.filter_by(user_name=user_name).first()
    @classmethod
    def find_user(cls,**kwargs):
        return cls.query.filter_by(kwargs=kwargs).first()
#go to utils
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_name': self.user_name}).decode('utf-8')
#go to utils
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_name = s.loads(token)['user_name']
        except:
            return None
        return User.query.filter_by(user_name=user_name).first()
