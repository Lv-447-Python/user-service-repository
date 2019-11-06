"""Model for user-service"""
from user_service import db
from flask_security import UserMixin
import datetime
from user_service import bcrypt
from flask import session


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

    def __init__(self, user_name, user_email, user_password, user_first_name,
                 user_last_name, user_image_file):
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_image_file = user_image_file

    @classmethod
    def find_by_user_name(cls,user_name):
        return cls.query.filter_by(user_name=user_name).first()

    def create_new_password(self):
        return bcrypt.generate_password_hash(self.user_name,10)
