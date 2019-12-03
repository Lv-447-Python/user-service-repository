from user_service import APP
from user_service.views.authentication import LogoutResource
from user_service.views.user_profile import ProfileResource
from tests import BaseTest
from user_service.configs.logger import logger
import unittest


    # coverage report -m --skip-covered
# 47 all profile 20 auth 44
if __name__ == "__main__":
    logger.info("Running the tests...")
    unittest.main()


# user for login test
# 	{
#     "user_email": "example@gmail.com",
#     "user_first_name": "John",
#     "user_last_name": "Johnson",
#     "user_image_file": "path",
#     "user_name": "johnny123",
#     "user_password": "test123"
#     }
	

