from . import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), nullable=False, unique=True)
    gender = db.Column('gender', db.String(10), nullable=False)
    email = db.Column('email', db.String(50), nullable=False)
    password_hashed = db.Column('password_hashed', db.String(200), nullable=False)
    registered_on = db.Column('registered_on', db.DateTime, nullable=True)
    is_confirmed = db.Column('is_confirmed', db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column('confirmed_on', db.DateTime, nullable=True)
    is_matched = db.Column('is_matched', db.Boolean, nullable=False, default=False)
    otp = db.Column('otp', db.String(4), nullable=True)
    
    def __init__(self, username, gender, email, password_hashed, is_admin=False, is_confirmed=False, confirmed_on=None, is_matched=False, otp=None):
        self.username = username
        self.gender = gender
        self.email = email
        self.password_hashed = password_hashed
        self.registered_on = datetime.now()
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on
        self.is_matched = is_matched
        self.otp = otp
        
    def __repr__(self):
        return f'<User {self.username}>'