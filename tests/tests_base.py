import unittest
from user_service import APP, DB, MAIL

POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'UserDB',
    'host': 'db',
    'port': '5432',
}


class BaseTest(unittest.TestCase):
    def setUp(self):
        """"
        Method for app and database configuration.
        Returns:
            None
        """
        APP.config['TESTING'] = True
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%(user)s:\
        %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
        self.APP = APP.test_client()
        DB.create_all()
