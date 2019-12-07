import json
from user_service.configs.logger import logger

import unittest

import requests
from flask_api import status

from unittest import mock
from user_service import APP, DB, MAIL

class BaseTest(unittest.TestCase):
    def setUp(self):
        APP.config['TESTING'] = True
        APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:1234@127.0.0.1:5432/userdb'
        self.APP = APP.test_client()
        DB.create_all()

    def test_valid_user_registration(self): #+
        response=self.APP.post('/profile', json= 		{
                                                        "user_email": "onlyfortest@gmail.com",
                                                        "user_first_name": "firstnamename",
                                                        "user_last_name": "lastname",
                                                        "user_image_file": "path",
                                                        "user_name": "name",
                                                        "user_password": "password"
                                                        })
        self.assertEqual(response.status, '200 OK')

    def test_invalid_user_registration_user_already_exists(self): #+
        response=self.APP.post('/profile', json={
                                                    
                                                    "user_email": "example@gmail.com",
                                                    "user_first_name": "Bob",
                                                    "user_last_name": "Johnson",
                                                    "user_image_file": "path",
                                                    "user_name": "johnny123",
                                                    "user_password": "test123"
                                                    
                                                        })
        self.assertEqual(response.status, '409 CONFLICT')

    
    
    def test_invalid_user_registration_invalid_data(self): #+
        response=self.APP.post('/profile', json={
                                                    "user_first_name": "111",
                                                    "user_last_name": "111",
                                                    "user_image_file": "1",
                                                    "user_name": "11",
                                                    "user_password": "11"

                                                    } )
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_invalid_user_registration_database_error(self): #???
        pass

    def test_user_profile_get_unauthorized(self): #+
        response=self.APP.get('/profile')
        self.assertEqual(response.status, '401 UNAUTHORIZED')

    def test_user_profile_get_success(self): #invalid login
        response_login=self.APP.post('/login', json=    {
                                                            "user_name": "johnny123",
                                                            "user_password": "test123"
                                                         }  
                                            )
        if response_login.status =='200 OK':
            response=self.APP.get('/profile')
            self.assertEqual(response.status, '200 OK')
            self.APP.get('/logout')
    # def test_user_profile_get_invalid_data(self):
    #     response_login=self.APP.post('/login', json=    {
    #                                                         "user_name": "johnny123",
    #                                                         "user_password": "test123"
    #                                                      } )
    #     if response_login.status =='200 OK':
    #         response=self.APP.put('/profile', data= 	{
    #                                                     "user_email": "example@gmail.com",
    #                                                     "user_first_name": "Bobby",
    #                                                     "user_last_name": "Johnson",
    #                                                     "user_image_file": "path",
    #                                                     "user_name": "johnny123",
    #                                                     "user_password": "test123"
    #                                                     })
    #         self.assertEqual(response.status, '400 BAD REQUEST')

    
    def test_user_profile_get_session_expired(self):
        pass

    def test_user_profile_get_invalid_data(self): #invalid login
        response_login=self.APP.post('/login', json=    {
                                                            "user_name": "johnny123",
                                                            "user_password": "test123"
                                                         }  
                                            )
        if response_login.status =='200 OK':
            response=self.APP.put('/profile', data={
                                                        "user_email": "example@gmail.com",
                                                        "user_first_name": "Bobby",
                                                        "user_last_name": "Johnson",
                                                        "user_image_file": "path",
                                                        "user_name": "johnny123",
                                                        "user_password": "test123"
                                                        

                                                        } )
            self.assertEqual(response.status, '400 BAD REQUEST')
            self.APP.get('/logout')


    # def test_user_profile_edit_user_does_not_exist(self):
    #     response=self.APP.put('/profile', json={
    #                                                 "user_email": "te@gmail.com",
    #                                                 "user_first_name": "t",
    #                                                 "user_last_name": "K",
    #                                                 "user_image_file": "path",
    #                                                 "user_name": "k123",
    #                                                 "user_password": "test123"

    #                                                 } )
    #     self.assertEqual(response.status, '400 BAD REQUEST')

    def test_user_profile_get_success(self): #invalid login go to db and choose user that already esists for these tests
        response_login=self.APP.post('/login', json=    {
                                                            "user_name": "johnny123",
                                                            "user_password": "test123"
                                                         } )
        if response_login.status =='200 OK':
            response=self.APP.put('/profile', json= 	{
                                                        "user_email": "example@gmail.com",
                                                        "user_first_name": "Bobby",
                                                        "user_last_name": "Johnson",
                                                        "user_image_file": "path",
                                                        "user_name": "johnny123",
                                                        "user_password": "test123"
                                                        })
            self.assertEqual(response.status, '200 OK')
            self.APP.put('/profile', json= 	{
                                                        "user_email": "example@gmail.com",
                                                        "user_first_name": "Bob",
                                                        "user_last_name": "Johnson",
                                                        "user_image_file": "path",
                                                        "user_name": "johnny123",
                                                        "user_password": "test123"
                                                        })
            self.APP.get('/logout')



    def test_user_profile_edit_session_expired(self):
        response=self.APP.put('/profile', json= 	{
                                                    "user_email": "example@gmail.com",
                                                    "user_first_name": "Bob",
                                                    "user_last_name": "Johnson",
                                                    "user_image_file": "path",
                                                    "user_name": "johnny123",
                                                    "user_password": "test123"
                                                    })
        self.assertEqual(response.status, '401 UNAUTHORIZED')

    def test_user_profile_edit_database_error(self):
        pass





    def test_user_profile_delete_unauthorized(self): #+
        response=self.APP.delete('/profile')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
    
    def test_user_profile_delete_authorized(self): #+
        response_login=self.APP.post('/login', json=    {
                                                            "user_name": "name",
                                                            "user_password": "password"
                                                         }  
                                            )
        if response_login.status =='200 OK':
            response=self.APP.delete('/profile')
            self.assertEqual(response.status, '200 OK')
            self.APP.get('/logout')

    def test_authentucation_login_success(self):
        response=self.APP.post('/login', json=    {
                                                            "user_name": "johnny123",
                                                            "user_password": "test123"
                                                         })
        self.assertEqual(response.status, '200 OK')                                            

    def test_authentucation_login_missing_data(self): #+
        response=self.APP.post('/login', json=    {
                                                            "user_password": "test123"
                                                         })
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_authentucation_login_invalid_data(self):
        response=self.APP.post('/login', data=    {
                                                            "user_name": "1111111111111111111111111111111111",
                                                            "user_password": "1111111111111111111111111111111111"
                                                         })
        self.assertEqual(response.status, '400 BAD REQUEST')

    def test_authentucation_login_invalid_login_or_password(self):
        response=self.APP.post('/login', json=    {
                                                            "user_name": "johnny123",
                                                            "user_password": "qqq"
                                                         })
        self.assertEqual(response.status, '400 BAD REQUEST')



