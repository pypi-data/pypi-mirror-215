'''
This module contains view functions for the maillib package.

Functions:
    -home(request): Accepts input from the `maillib/home.html` template form
        and checks the validity of the receiver email address. If the email address
        is valid, the email is sent to the recepient and a status message is shown
        to the sender. If the email address is invalid, the email is not sent, and
        the error message is shown to the user.

Constants:
    -API_KEY: This is stored as an environment variable for security
    -VALIDATE_URL: This is the endpoint called to validate the email address
    -SEND_MAIL_URL: Upon successful validation, this is the endpoint called to
    send the email to the specified email address.
'''

import os
from django.shortcuts import render
from django.contrib import messages
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
VALIDATE_URL = f'https://100085.pythonanywhere.com/api/v1/mail/{API_KEY}/?type=validate'
SEND_MAIL_URL = f'https://100085.pythonanywhere.com/api/v1/mail/{API_KEY}/?type=send-email'

def home(request):

    """
    Renders the home page and handles the submission of the email form form
    `templates/home.html`.

    If the HTTP request method is POST, this function extracts the form data from
    the request object and sends it to a validation API.
    If the validation API returns a success response, the email sending API is called
    with the form data. If the email sending API returns a success response, a success
    message is added to the messages framework. Otherwise, an error message is added. The message
    is then displayed back to the user in the home.html.

    Args: 
        request (HttpRequest): The HTTP request object.

    Variables:
        API_KEY(str): A string containig the api key stored in the .env file
        VALIDATE_URL(str): a string containing the validation url endpoint
        SEND_MAIL_URL(str): a string containing the send email url endpoint

    Returns:
        HttpResponse: A rendered HTML template for the home page with any messages from form submission.
    """

    if request.method== "POST":

        body = {
            "email": request.POST.get('toEmail'),
            "name":request.POST.get('fullName'),
            "fromName":request.POST.get('fullName'),
            "fromEmail" : request.POST.get('fromEmail'),
            "subject" : request.POST.get('subject'),
            "body" : request.POST.get('message')
        }

        response_from_validation_call = requests.post(VALIDATE_URL, json=body)
        validate_response = response_from_validation_call.json()

        if validate_response['success'] is True:
            response_from_email_call = requests.post(SEND_MAIL_URL, json=body)
            mail_response = response_from_email_call.json()

            if mail_response['success'] is True:
                messages.add_message(request, messages.INFO, mail_response['message'])
            else:
                messages.add_message(request, messages.ERROR, mail_response['message'])

        else:
            messages.add_message(request, messages.ERROR, validate_response['message'])

    return render(request, 'maillib/home.html')
