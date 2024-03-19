from itsdangerous import URLSafeTimedSerializer
from flask import Flask
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECURITY_PASSWORD_SALT'
app.config['SECURITY_PASSWORD_SALT'] = 'SECURITY_PASSWORD_SALT'

def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    
    try:    
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False
    
def generate_OTP():
    arr = []
    for i in range(4):
        a = random.randint(0, 10)
        arr.append(a)
    return arr