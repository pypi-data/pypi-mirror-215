import os
from django.test import Client, TestCase
from django.urls import reverse
import requests
from dotenv import load_dotenv

load_dotenv()


class TestViews(TestCase):
    '''
    Test cases for the maillib view in the maillib Django app.

    Methods:
    - setUp: Initializes the client object to simulate a web browser and the reverse function
                stored in home_url, used to get the home view.
    - test_should_show_home_page: Tests that the home view successfully loads the home.html template.
    - test_email_validate: tests that the validate url call returns a 200 status code and that the 
        template used is home.html
    - test_valid_email: Tests that the API call to the validate email endpoint returns success=True if the email
        provided is valid
    - test_send_email: Tests that the API call to the send email endpoint sends an email successfully and returns
        success=True
    '''

    def setUp(self):
        '''
        Initializes the client object to simulate a web browser and the reverse function stored in home_url, used to get the home view.
        '''
        self.client = Client()
        self.home_url = reverse('home')
    
    def test_should_show_home_page(self):
        '''
        Tests that the home view successfully loads the home.html template.
        '''
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "maillib/home.html")

    def test_email_validate(self):
        '''
         tests that the validate url call returns a 200 status code and that the 
         template used is home.html
        '''
        response = self.client.post(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'maillib/home.html')

    def test_valid_email(self):
        '''
        Tests that the API call to the validate email endpoint returns success=True if the email
        provided is valid
        '''
        data = {
            "email":"marvinwandabwa0@gmail.com",
            "name":"Marvin",
            "fromName":"Marvin Okwaro",
            "fromEmail" : "marvin.wekesa@gmail.com",
            "subject" : "Final mail test",
            "body" : "I am sending as a test mail"
        }
        api_key = os.getenv('API_KEY')
        url = f'https://100085.pythonanywhere.com/api/v1/mail/{api_key}/?type=validate'

        response = requests.post(url, json=data)
        valid_resp = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(valid_resp['success'], True)
        


    def test_send_email(self):
        '''
        Tests that the API call to the send email endpoint sends an email successfully and returns
        success=True
        '''
        data = {
            "email":"marvinwandabwa0@gmail.com",
            "name":"Marvin",
            "fromName":"Marvin Okwaro",
            "fromEmail" : "marvin.wekesa@gmail.com",
            "subject" : "Final mail test",
            "body" : "I am sending as a test mail"
        }
        api_key = os.getenv('API_KEY')
        url = f'https://100085.pythonanywhere.com/api/v1/mail/{api_key}/?type=send-email'

        response = requests.post(url, json=data)
        email_resp = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(email_resp['success'], True)