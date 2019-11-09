from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from user_service import app
from user_service.models.user import User


def get_reset_token(object, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_name': object.user_name}).decode('utf-8')


def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        user_name = s.loads(token)['user_name']
    except:
        return None
    return User.query.filter_by(user_name=user_name).first()