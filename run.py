from user_service import APP
from user_service.views.authentication import LogoutResource
from user_service.views.user_profile import ProfileResource

if __name__ == '__main__':
    APP.run(debug=True)
