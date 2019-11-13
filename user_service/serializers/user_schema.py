"""Schema for user-service"""
from user_service import marshmallow
from marshmallow import fields
from user_service.models.user import User


class UserSchema(marshmallow.Schema):
    id = fields.Integer(dump_only=True)
    user_name = fields.Str()
    user_email = fields.Str()
    user_password = fields.Str()
    user_first_name = fields.Str()
    user_last_name = fields.Str()
    user_image_file = fields.Str()
    user_registration_data = fields.DateTime(dump_only=True)


class LoginSchema(marshmallow.Schema):
    user_name = fields.Str()
    user_password = fields.Str()
