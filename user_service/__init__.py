"""Initial file with main settings"""
# import POSTGRES as POSTGRES
import smtplib

from flask import Flask
# from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

APP = Flask(__name__)
API = Api(APP)

# CORS(APP, supports_credentials=True)

BCRYPT = Bcrypt(APP)

POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'UserDB',
    'host': 'db',
    'port': '5432',
}

JWT = JWTManager(APP)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
APP.config['SECRET_KEY'] = 'jwt-secret-string'
APP.config['JWT_TOKEN_LOCATION'] = ['cookies']


APP.config['MAIL_SERVER'] = 'smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USE_SSL'] = True
APP.config['MAIL_USERNAME'] = 'testingforserve@gmail.com'
APP.config['MAIL_PASSWORD'] = 'StrongPassword98'


MAIL = Mail(APP)

DB = SQLAlchemy(APP)
MARSHMALLOW = Marshmallow(APP)
MIGRATE = Migrate(APP, DB)
MANAGER = Manager(APP)
MANAGER.add_command('db', MigrateCommand)
from user_service.models.user import User