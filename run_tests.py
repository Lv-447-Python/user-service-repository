from user_service import APP
from user_service.views.authentication import LogoutResource
from user_service.views.user_profile import ProfileResource
from user_service.views.user_profile import ResetPasswordRequestResource
from tests.tests_base import BaseTest
from tests.tests_for_user_service import TestsForUserService
from user_service.configs.logger import logger
import unittest

#coverage run run_tests.py
# coverage report -m --skip-covered

if __name__ == "__main__":
    logger.info("Running the tests...")
    unittest.main()

