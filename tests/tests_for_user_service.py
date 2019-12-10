import json
from user_service.configs.logger import logger

import unittest

import requests
from flask_api import status

from user_service import APP, DB, MAIL
from tests.tests_base import BaseTest


class TestsForUserService(BaseTest):

    def test_valid_user_registration(self): #+
        with open('tests/request_files/valid_user_reg.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/profile', json=data)
            self.assertEqual(response.status, '200 OK')

    def test_invalid_user_registration_user_already_exists(self): #+
        with open('tests/request_files/invalid_user_reg_user_exists.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/profile', json=data)
            self.assertEqual(response.status, '409 CONFLICT')

    
    
    def test_invalid_user_registration_invalid_data(self): #+
        with open('tests/request_files/invalid_user_reg_invalid_data.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/profile', json=data)
            self.assertEqual(response.status, '400 BAD REQUEST')

   
    def test_invalid_user_registration_database_error(self): #+
        with open('tests/request_files/invalid_user_reg_db_error.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/profile', json=data)
            self.assertEqual(response.status, '400 BAD REQUEST') 
        

    def test_user_profile_get_unauthorized(self): #+
        response=self.APP.get('/profile')
        self.assertEqual(response.status, '401 UNAUTHORIZED')

    def test_user_profile_get_success(self): #invalid login
         with open('tests/request_files/login_success.json', 'r') as data_login:
            data_login = json.loads(data_login.read())
            response_login=self.APP.post('/login', json=data_login)
            if response_login.status =='200 OK':
                response=self.APP.get('/profile')
                self.assertEqual(response.status, '200 OK')
                self.APP.get('/logout')
    
    # def test_user_profile_get_session_expired(self):
    #     pass

    def test_user_profile_edit_invalid_data(self): #+
        with open('tests/request_files/login_success.json', 'r') as data_login:
            data_login = json.loads(data_login.read())
            response_login=self.APP.post('/login', json=data_login)
            with open('tests/request_files/edit_valid_data.json', 'r') as data_file:
                data_file = json.loads(data_file.read())
                if response_login.status =='200 OK':
                    response=self.APP.put('/profile', data=data_file )
                    self.assertEqual(response.status, '400 BAD REQUEST')
                    self.APP.get('/logout')


    def test_user_profile_edit_user_does_not_exist(self):
        with open('tests/request_files/edit_user_do_not_exist.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.put('/profile', json=data )
            self.assertEqual(response.status, '401 UNAUTHORIZED')

    def test_user_profile_edit_success(self): #+
        with open('tests/request_files/login_success.json', 'r') as data_login:
            data_login = json.loads(data_login.read())
        response_login=self.APP.post('/login', json=data_login)
        if response_login.status =='200 OK':
             with open('tests/request_files/edit_valid_data.json', 'r') as data_file:
                data_file = json.loads(data_file.read())
                response=self.APP.put('/profile', json=data_file)
                self.assertEqual(response.status, '200 OK')
                with open('tests/request_files/edit_previous_data.json', 'r') as data:
                    data = json.loads(data.read())
                    self.APP.put('/profile', json=data)
                    self.APP.get('/logout')



    def test_user_profile_edit_session_expired(self): #+
        with open('tests/request_files/invalid_user_reg_user_exists.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.put('/profile', json=data)
            self.assertEqual(response.status, '401 UNAUTHORIZED')

    # def test_user_profile_edit_database_error(self):
    #     pass





    def test_user_profile_delete_unauthorized(self): #+
        response=self.APP.delete('/profile')
        self.assertEqual(response.status, '401 UNAUTHORIZED')
    
    def test_user_profile_delete_authorized(self): #+

        with open('tests/request_files/delete_success.json', 'r') as data:
            data = json.loads(data.read())
            response_login=self.APP.post('/login', json=data)
            if response_login.status =='200 OK':
                response=self.APP.delete('/profile')
                self.assertEqual(response.status, '200 OK')
                self.APP.get('/logout')

    def test_authentication_login_success(self):#+
        with open('tests/request_files/login_success.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/login', json=data)
            self.assertEqual(response.status, '200 OK')                                            

    def test_authentication_login_missing_data(self): #+
        with open('tests/request_files/login_missing_data.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/login', json=data)
            self.assertEqual(response.status, '400 BAD REQUEST')

    def test_authentication_login_invalid_data(self):
        with open('tests/request_files/login_invalid_data.json', 'r') as data_file:
            data_file = json.loads(data_file.read())
            response=self.APP.post('/login', data=data_file)
            self.assertEqual(response.status, '400 BAD REQUEST')

    def test_authentication_login_invalid_login_or_password(self): #+
        with open('tests/request_files/login_invalid_login_or_password.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/login', json=data)
            self.assertEqual(response.status, '400 BAD REQUEST')



    def test_edit_profile_db_error(self):
        with open('tests/request_files/edit_login.json', 'r') as data:
            data = json.loads(data.read())
            response_login=self.APP.post('/login', json=data)
            if response_login=='200 OK':
                with open('tests/request_files/edit_profile_db_error.json', 'r') as data_file:
                    data_file = json.loads(data.read())
                    response=self.APP.put('/profile', json=data_file)
                    self.assertEqual(response.status, '400 BAD REQUEST')



    # # def test_send_email_runtime_error(self):

    def test_reset_password_post_invalid_data(self): #+
        with open('tests/request_files/reset_pass_post_invalid_data.json', 'r') as data_file:
            data_file = json.loads(data_file.read())
            response=self.APP.post('/reset-password', data=data_file)
            self.assertEqual(response.status, '400 BAD REQUEST')

    
    def test_reset_password_post_success(self):
        with open('tests/request_files/reset_pass_success.json', 'r') as data:
            data = json.loads(data.read())
            response=self.APP.post('/reset-password', json=data)
            self.assertEqual(response.status, '200 OK')

    def test_authentication_check_success(self):
        with open('tests/request_files/login_success.json', 'r') as data:
            data = json.loads(data.read())
            response_login=self.APP.post('/login', json=data)
            if response_login.status=='200 OK':
                response=self.APP.get('/auth')
                self.assertEqual(response.status, '200 OK')
    
    def test_authentication_check_invalid(self):
        response=self.APP.get('/auth')
        self.assertEqual(response.status, '401 UNAUTHORIZED')




    # def test_reset_password_post_no_user_with_this_email(self):
    #     with open('tests/request_files/reset_pass_post_invalid_data.json', 'r') as data:
    #         data = json.loads(data.read())
    #         response=self.APP.post('/reset-password', json=data)
    #         self.assertEqual(response.status, '400 BAD REQUEST')

    # def test_reset_password_put_success(self):
    #     response_post=self.APP.post('/reset-password', json= {
    #                                                         "user_email": "ma.maaravi@gmail.com"
    #                                                     })
    #     self.assertEqual(response.status, '200 OK')
    #     if response_post=='200 OK':
    #         response=self.APP.put(API.url_for(ResetPasswordRequestResource, token=)


    # def test_reset_password_put_timeout_error(self):

    # def test_reset_password_put_invalid_data(self):
    



