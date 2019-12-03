"""Utils for user service"""
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from user_service import APP
from user_service.models.user import User
from user_service.configs.logger import logger


def get_reset_token(user, expires_sec=1800):
    """
    Create a specify token for reset user password
    Args:
        user
        expires_sec

    Returns:
        token: string
    """
    hash_token_password = Serializer(APP.config['SECRET_KEY'], expires_sec)
    logger.info("Successful call of a get_reset_token function")
    return hash_token_password.dumps({'user_name': user.user_name}).decode('utf-8')


def verify_reset_token(token):
    """
    Find user by token
    Args:
        token

    Returns:
        instance of User or None
    """
    hash_token_password = Serializer(APP.config['SECRET_KEY'])
    try:
        user_name = hash_token_password.loads(token)['user_name']
    except SignatureExpired:
        logger.error("URL signature is expired")
        return None
    logger.info("Successful call of a verify_reset_token function")
    return User.query.filter_by(user_name=user_name).first()
