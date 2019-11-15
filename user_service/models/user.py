"""Model for user-service"""
import datetime
from flask_security import UserMixin
from sqlalchemy import Column, Integer, String, DateTime
from user_service import DB


class User(DB.Model, UserMixin):
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(25), nullable=False, unique=True)
    user_email = Column(String(35), nullable=False, unique=True)
    user_password = Column(String(255), nullable=False)
    user_first_name = Column(String(25), nullable=False)
    user_last_name = Column(String(25), nullable=False)
    user_image_file = Column(String(25), nullable=False)
    user_registration_data = Column(DateTime, nullable=False, default=datetime.datetime.now())

    @classmethod
    def find_user(cls, **kwargs):
        """
        Function for find user by some argument
        Args:
            **kwargs:

        Returns:
            instance of user or None if user not found
        """
        return cls.query.filter_by(**kwargs).first()
