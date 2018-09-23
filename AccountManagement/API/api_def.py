from flask_restplus import fields
from AccountManagement.API.api_var import api

new_user = api.model('The new data for registering a new user', {
    'username': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email Address of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'newsletter': fields.Boolean(required=True, description='If the user wants newsletter emails')
})

successful = api.model('Indicates if a call has resulted in a success', {
    'success': fields.Boolean(required=True, description='If successful or not'),
    'message': fields.String(description='Message to be displayed')
})

login_data = api.model('The login information for logging a user in', {
    'username': fields.String(required=True, description='Username of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

token = api.model('Login Token for game and website', {
    'userid': fields.Integer(required=True, description='ID of the user'),
    'token': fields.String(required=True, description='~One time password for accessing resources.'),
    'session_token': fields.String(required=True, description='Token for denying DDoS')
})

email_address = api.model('The email address of the user', {
    'email': fields.String(required=True, description='The email address of the user (who would have guessed).')
})

email_token = api.model('Token to activate the email address', {
    'email_token': fields.String(
        required=True,
        description='Token for completing the registration and activating the email address'
    )
})

reset_password = api.model('Data to reset your password in case you forgot', {
    'email_token': fields.String(
        requried=True,
        description='The token sent to the user via mail for unforgeable requests'
    ),
    'new_password': fields.String(required=True, description='The new password')
})

userdetails = api.model('Request-Data to update user data', {
    'token': fields.Nested(token, required=True),
    'old_password': fields.String(required=True, description='The old password to validate the request'),
    'email': fields.String(required=False, description='The new email address'),
    'new_password': fields.String(required=False, description='The new password'),
    'new_password2': fields.String(required=False, description='Retyped new password vs. typos'),
    'newsletter': fields.Boolean(required=False, description='If newsletters shall be sent or not')
})

user_data = api.model('User Data', {
    'username': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email Address of the user'),
    'newsletter': fields.Boolean(required=True, description='If the user wants newsletter emails')
})