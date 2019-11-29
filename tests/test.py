# import json
# import logging
# import logging.config
# import unittest
# import os
# from flask_jwt_extended import create_access_token
# from marshmallow import ValidationError
# from flask_restful import Resource
# from flask_api import status
# from flask import jsonify, request, session, make_response
# from user_service.serializers.user_schema import LoginSchema
# from user_service import API
# from user_service.models.user import User
# from user_service import BCRYPT

# from user_service import APP, DB, MAIL

# logging.config.fileConfig('/Python Projects/user-service-repository/user_service/configs/logger.conf')
# logger = logging.getLogger('userServiceApp')

 
# class MyTestCase(unittest.TestCase):
#     def setUp(self):
#         APP.config['TESTING'] = True
#         APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:1234@127.0.0.1:5432/user_service_test'
#         self.APP = APP.test_client()
#         DB.create_all()

#     def test_base_service(self):
#         response = self.APP.get('/')
#         self.assertEqual(response.status, '200 OK')

 
#     def test_main_page(self):
#         response = self.APP.get('/', follow_redirects=True)
#         self.assertEqual(response.status, 200)

#     def test_valid_user_registration(self):
#         response=self.APP.post('/profile', data={
#                                                     "user_email": "ma.maaravi1@gmail.com",
#                                                     "user_first_name": "Marta",
#                                                     "user_image_file": "path",
#                                                     "user_name": "marta123",
#                                                     "user_password": "qwerty123"

#                                                     } )
#         self.assertEqual(response.status, 'HTTP_201_CREATED')

#     def test_invalid_user_registration_user_already_exists(self):
#         response=self.APP.post('/profile', data={
#                                             "user_email": "ma.maaravi1@gmail.com",
#                                             "user_first_name": "Marta",
#                                             "user_image_file": "path",
#                                             "user_name": "marta123",
#                                             "user_password": "qwerty123"

#                                             } )
#         self.assertEqual(response.status, 'HTTP_409_CONFLICT')

#     def test_invalid_user_registration_invalid_data(self):
#         response=self.APP.post('/profile', data={
#                                             "user_email": "123",
#                                             "user_first_name": "111",
#                                             "user_image_file": "1",
#                                             "user_name": "11",
#                                             "user_password": "11"

#                                             } )
#         self.assertEqual(response.status, 'HTTP_400_BAD_REQUEST')

        