"""Schema for user-service"""
from user_service import marshmallow
from user_service.models.user import User
from marshmallow import Schema, fields


class UserSchema(marshmallow.ModelSchema):
    user_id = fields.Int(dump_only=True)
    user_name = fields.Str()
    user_email = fields.Email()
    user_password = fields.Str()
    user_first_name = fields.Str()
    user_last_name = fields.Str()
    user_image_file = fields.Url()
    user_registration_data = fields.DateTime(dump_only=True)
