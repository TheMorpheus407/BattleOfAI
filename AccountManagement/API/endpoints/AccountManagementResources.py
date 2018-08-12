from flask_restplus import Namespace, Resource
from flask import request

import string

from AccountManagement.API.api_var import api
from AccountManagement.API.api_def import user_data, userdetails, new_user, successful, login_data, token, email_address, email_token, reset_password

from AccountManagement.Database.UserDTO import UserDTO
from AccountManagement.Database.db import db

from AccountManagement.Utils.Sendmail import send_registration_mail, send_pwforgot_email
from AccountManagement.Utils.CleanUp import delete_trash_accounts

accnamespace = Namespace('iam/', description='Identity and Access Management for Battle of AI')

@accnamespace.route('/register')
class RegisterResource(Resource):
    @api.expect(new_user)
    @api.marshal_with(successful)
    def post(self):
        delete_trash_accounts()
        data = request.json
        if UserDTO.query.filter_by(username=data['username']).first() is not None:
            return {'success': False, 'message': 'User already exists.'}
        user = UserDTO(data['username'], data['email'], data['password'], data['newsletter'])
        db.session.add(user)
        db.session.commit()
        send_registration_mail(user.email, user.email_token)
        return {'success': True, 'message': 'Please check your emails.'}

@accnamespace.route('/verifyEmail')
class VerifyEmail(Resource):
    @api.expect(email_token)
    @api.marshal_with(successful)
    def post(self):
        token = request.json['email_token']
        user = UserDTO.query.filter_by(email_token=token).first()
        if user is None and user.email_token_valid():
            return {'success': False, 'message': 'User not found or email already verified.'}
        user.verify_email()
        return {'success': True, 'message': 'User successfully verified.'}

@accnamespace.route('/login')
class LoginResource(Resource):
    @api.expect(login_data)
    @api.marshal_with(token)
    def post(self):
        user = UserDTO.query.filter_by(username=request.json['username']).first()
        if user is None:
            return None
        if not user.check_password(request.json['password']) or not user.is_verified():
            return None
        token, sesstoken = user.token, user.session_token
        if not user.check_token(token, sesstoken):
            token, sesstoken = user.generate_tokens()
        return {'userid': user.id, 'token': token, 'session_token': sesstoken}

@accnamespace.route('/forgotPassword')
class ForgotPasswordResource(Resource):
    @api.expect(email_address)
    def post(self):
        user = UserDTO.query.filter_by(email=request.json['email']).first()
        if user is not None:
            user.gen_pwforgot_password()
            send_pwforgot_email(user.email, user.email_token)

@accnamespace.route('/resetPassword')
class ResetPasswordResource(Resource):
    @api.expect(reset_password)
    @api.marshal_with(successful)
    def post(self):
        user = UserDTO.query.filter_by(email_token=request.json['email_token']).first()
        if user is None or not user.email_token_valid():
            return {'success': False, 'message': 'User not found or token invalid.'}
        user.change_password(request.json['new_password'])
        return {'success': True, 'message': 'Password successfully changed You can now go back and log in.'}

@accnamespace.route('/validateToken')
class ValidateTokenResource(Resource):
    @api.expect(token)
    @api.marshal_with(successful)
    def post(self):
        user = UserDTO.query.filter_by(id=request.json['userid']).first()
        if user is not None and user.check_token(request.json['token'], request.json['session_token']):
            return {'success': True, 'message': 'Logged in successfully.'}
        return {'success': False, 'message': 'Your token is invalid. Consider logging in again.'}

@accnamespace.route('/refreshToken')
class RefreshTokenResource(Resource):
    @api.expect(token)
    @api.marshal_with(token)
    def post(self):
        user = UserDTO.query.filter_by(id=request.json['userid']).first()
        if user is not None and user.check_token(request.json['token'], request.json['session_token']):
            token, sesstoken = user.generate_tokens()
            return {'userid': user.id, 'token': token, 'session_token': sesstoken}
        return None

@accnamespace.route('/updateUser')
class UpdateUserResource(Resource):
    @api.expect(userdetails, validate=False)
    @api.marshal_with(successful)
    def post(self):
        print(request.json)
        id = request.json['token']['userid']
        user = UserDTO.query.filter_by(id=id).first()
        failed_msg = {'success': False, 'message': 'Something went wrong, couldn\'t verify you. Please log in again.'}
        if user is None or not user.check_token(request.json['token']['token'], request.json['token']['session_token']):
            return failed_msg
        if not user.check_password(request.json['old_password']) or not user.is_verified():
            return failed_msg
        if 'new_password' in request.json and 'new_password2' in request.json:
            new_password = request.json['new_password']
            new_password2 = request.json['new_password2']
            if new_password is not None and (new_password2 is None or any(char in new_password for char in string.digits) or any(char in new_password for char in string.ascii_uppercase) or any(char in new_password for char in string.punctuation) or new_password == new_password2):
                return {'success': False, 'message': 'Please check your password again, seems like they either did not match or your password is too weak.'}
            if new_password is not None:
                user.change_password(new_password)
        if 'email' in request.json and request.json['email'] is not None:
            user.set_email(request.json['email'])
        if 'newsletter' in request.json and request.json['newsletter'] is not None:
            user.set_newsletter(request.json['newsletter'])
        return {'success': True, 'message': 'Updated all your data accordingly.'}

@accnamespace.route('/getUserByID/<int:id>')
class GetUserByIdResource(Resource):
    @api.expect(token)
    @api.marshal_with(user_data)
    def post(self, id):
        user = UserDTO.query.filter_by(id=id).first()
        if user is None or not user.check_token(request.json['token'], request.json['session_token']):
            return None
        return {'username': user.username, 'email': user.email, 'newsletter': user.newsletter}