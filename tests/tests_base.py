import unittest
from user_service import APP, DB, MAIL


class BaseTest(unittest.TestCase):
    def setUp(self):
        APP.config['TESTING'] = True
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:1234@127.0.0.1:5432/userdb'
        self.APP = APP.test_client()
        DB.create_all()