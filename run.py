from user_service import APP
from user_service.views.authentication import LogoutResource
from user_service.views.user_profile import ProfileResource
import logging
import logging.config

logging.config.fileConfig('/Python Projects/user-service-repository/user_service/configs/logger.conf')
logger = logging.getLogger('userServiceApp')

if __name__ == '__main__':
    logger.info("Running the app...")
    APP.run(debug=True)