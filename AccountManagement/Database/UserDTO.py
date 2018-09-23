from AccountManagement.Database.db import db
import bcrypt
import secrets
from datetime import datetime, timedelta


class UserDTO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.LargeBinary)
    newsletter = db.Column(db.Boolean)
    email_verified = db.Column(db.Boolean)
    email_token = db.Column(db.String(300))
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    email_token_generated_time = db.Column(db.DateTime)

    token = db.Column(db.String(300))
    session_token = db.Column(db.String(300))
    token_generated_time = db.Column(db.DateTime)

    def __init__(self, username, email, password, newsletter):
        self.username = username
        self.email = email
        self.password = self.password_to_hash(password)
        self.newsletter = newsletter
        self.email_verified = False
        self.email_token = self.generate_independent_token()
        self.email_token_generated_time = datetime.now()

        self.token = None
        self.session_token = None

    def verify_email(self):
        self.email_token = None
        self.email_verified = True
        self.email_token_generated_time = None
        db.session.commit()

    # TODO shouldn't this method be static
    def password_to_hash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, to_check):
        return bcrypt.checkpw(to_check.encode('utf-8'), self.password)

    # TODO shouldn't this method be static
    def generate_independent_token(self):
        token = secrets.token_urlsafe(192)
        if len(token) > 256:
            token = token[0:255]
        return token

    def generate_tokens(self):
        self.token = self.generate_independent_token()
        self.session_token = self.generate_independent_token()
        self.token_generated_time = datetime.now()
        db.session.commit()
        return self.token, self.session_token

    def gen_pwforgot_password(self):
        self.email_token = self.generate_independent_token()
        self.email_token_generated_time = datetime.now()
        db.session.commit()
        return self.email_token

    def change_password(self, password):
        self.email_token = None
        self.email_token_generated_time = None
        self.password = self.password_to_hash(password)
        db.session.commit()

    def email_token_valid(self):
        return self.email_token_generated_time > (datetime.now() - timedelta(days=1))

    def check_token(self, token, session_token):
        if token is None or session_token is None:
            return False
        if not session_token == self.session_token:
            return False
        if not self.token_generated_time > (datetime.now() - timedelta(days=1)):
            return False
        if not token == self.token:
            self.session_token = None
            self.token = None
            db.session.commit()
            return False
        return True

    def is_verified(self):
        return self.email_verified

    def can_be_trashed(self):
        return not self.email_verified and not self.email_token_valid()

    def set_email(self, email):
        self.email = email
        db.session.commit()

    def set_newsletter(self, newsletter):
        self.newsletter = newsletter
        db.session.commit()

    @staticmethod
    def validate_email(email):
        email = email.split("@")
        if not len(email) == 2:
            return False
        email = email[1].split('.')
        if len(email) < 2: #foo@abcde
            return False
        return True
