from user_service import APP
from user_service.views.authentication import LogoutResource
from user_service.views.user_profile import ProfileResource
from user_service.configs.logger import logger

if __name__ == '__main__':
    logger.info("Running the app...")
    APP.run(debug=True)