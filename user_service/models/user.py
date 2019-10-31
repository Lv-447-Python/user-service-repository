"""Model for user-service"""
from user_service import db
from flask_security import UserMixin


class User(db.Model, UserMixin):
    """ Represent database table user by class
    :param: integer id for user
    :param: string name for user
    :param: string email for user
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(15), nullable=False, unique=True)
    user_email = db.Column(db.String(15), nullable=False, unique=True) #EmailType
    user_password = db.Column(db.String(100), nullable=False)
    registration_data = db.Column(db.DateTime())
    # first name and last name?

    def __init__(self, user_name, user_email, user_password):
        self.user_name = user_name
        self.email = user_email
        self.user_password = user_password
