# import POSTGRES as POSTGRES
import smtplib

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
api = Api(app)

CORS(app)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:snoopy1@127.0.0.1:5432/UserDB'
app.config['SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME']= 'testingforserve@gmail.com'
app.config['MAIL_PASSWORD'] = 'StrongPassword98'


mail = Mail(app)

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
from user_service.models.user import User
