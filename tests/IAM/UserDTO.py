from sqlalchemy import Column, Integer, String, LargeBinary, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
import secrets
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///../AccountManagement/users.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class userDTO(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(LargeBinary)
    newsletter = Column(Boolean)
    email_verified = Column(Boolean)
    email_token = Column(String(255))
    registration_date = Column(DateTime, nullable=False, default=datetime.now())
    email_token_generated_time = Column(DateTime)

    token = Column(String(255))
    session_token = Column(String(255))
    token_generated_time = Column(DateTime)

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
        session.commit()

    def password_to_hash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, to_check):
        return bcrypt.checkpw(to_check.encode('utf-8'), self.password)

    def generate_independent_token(self):
        token = secrets.token_urlsafe(192)
        if len(token) > 256:
            token = token[0:255]
        return token

    def generate_tokens(self):
        self.token = self.generate_independent_token()
        self.session_token = self.generate_independent_token()
        self.token_generated_time = datetime.now()
        session.commit()
        return self.token, self.session_token

    def gen_pwforgot_password(self):
        self.email_token = self.generate_independent_token()
        self.email_token_generated_time = datetime.now()
        session.commit()
        return self.email_token

    def change_password(self, password):
        self.email_token = None
        self.email_token_generated_time = None
        self.password = self.password_to_hash(password)
        session.commit()

    def email_token_valid(self):
        return self.email_token_generated_time > (datetime.now() - timedelta(days=1))

    def check_token(self, token, session_token):
        if not session_token == self.session_token:
            return False
        if not self.token_generated_time > (datetime.now() - timedelta(days=1)):
            return False
        if not token == self.token:
            self.session_token = None
            self.token = None
            session.commit()
            return False
        return True

    def is_verified(self):
        return self.email_verified

    def can_be_trashed(self):
        return not self.email_verified and not self.email_token_valid()

    @staticmethod
    def validate_email(email):
        email = email.split("@")
        if not len(email) == 2:
            return False
        email = email[1].split('.')
        if len(email) < 2: #foo@abcde
            return False
        return True