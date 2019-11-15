"""Initial file with main settings"""
# import POSTGRES as POSTGRES
import smtplib

from flask import Flask
from flask_cors import CORS
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

CORS(APP, supports_credentials=True)

BCRYPT = Bcrypt(APP)

JWT = JWTManager(APP)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:snoopy1@127.0.0.1:5432/UserDB'
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
