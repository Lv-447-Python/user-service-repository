"""Model for user-service"""
from user_service import db
from flask_security import UserMixin
import datetime


class User(db.Model, UserMixin):
    """"""
    """ Represent database table user by class
    :param: integer id for user
    :param: string name for user
    :param: string email for user
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(15), nullable=False, unique=True)
    user_email = db.Column(db.String(15), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_first_name = db.Column(db.String(15), nullable=False)
    user_last_name = db.Column(db.String(15), nullable=False)
    user_image_file = db.Column(db.String(15), nullable=False)
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
