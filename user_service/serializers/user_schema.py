"""Schema for user-service"""
from user_service import ma
from user_service.models.user import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
