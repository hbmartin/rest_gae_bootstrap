import webapp2
import logging
import models

from sys import path
path.insert(1, './rest_gae')

from rest_gae import *
from rest_gae.users import UserRESTHandler

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

model_handlers = []
model_list = models.list_models()

# automatically create a handler for every model listed in models
for model_name in model_list:
    model_handlers.append(RESTHandler(
        '/api/' + model_name.lower(),
        getattr(models, model_name),
        permissions={
            'GET': PERMISSION_ANYONE,
            'POST': PERMISSION_LOGGED_IN_USER,
            'PUT': PERMISSION_OWNER_USER,
            'DELETE': PERMISSION_ADMIN
        },

        # Will be called for every PUT, right before the model is saved
        put_callback=lambda model, data: model
    ))

# add special users handler
if 'users' not in model_list:
    model_handlers.append(UserRESTHandler(
        '/api/users',
        user_details_permission=PERMISSION_OWNER_USER,
        verify_email_address=True,
        verification_email={
            'sender': 'John Doe <john@doe.com>',
            'subject': 'Verify your email address',
            'body_text': 'Click here {{ user.full_name }}: {{ verification_url }}',
            'body_html': '<a href="{{ verification_url }}">Click here</a> {{ user.full_name }}'
        },
        verification_successful_url='/verification_successful',
        verification_failed_url='/verification_failed',
        reset_password_url='/reset_password',
        reset_password_email={
            'sender': 'John Doe <john@doe.com>',
            'subject': 'Please reset your password',
            'body_text': 'Reset here: {{ verification_url }}',
            'body_html': '<a href="{{ verification_url }}">Click here</a> to reset'
        },
    ))

app = webapp2.WSGIApplication(model_handlers, debug=True, config=config)
