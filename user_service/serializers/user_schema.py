"""Schema for user-service"""
from user_service import marshmallow
from marshmallow import fields
from user_service.models.user import User


class UserSchema(marshmallow.ModelSchema):
    class Meta:
        model = User


class LoginSchema(marshmallow.Schema):
    user_name = fields.Str()
    user_password = fields.Str()
