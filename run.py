from user_service import app
from user_service.views.authentication import LogoutResource
from user_service.views.user_profile import ProfileResource

if __name__ == '__main__':
    app.run(debug=True)
