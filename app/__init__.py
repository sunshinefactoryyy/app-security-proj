from flask import Flask, render_template, request, escape
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
import stripe
from flask_socketio import SocketIO

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab2d494b73d4d8ee5ef8f28b5d575bcd'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config['JWT_SECRET_KEY'] = '864c7da95d444f5bbc5b3c651a140e09'
app.config.update(
    SESSION_COOKIE_SECURE=True, #only HTTPS traffic
    SESSION_COOKIE_HTTPONLY=True, #protects content of cookies from being read with javascript
    SESSION_COOKIE_SAMESITE='Lax', #prevents sending cookies with CSRF-prone requests from external sites(submitting form)
)
stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY'],
    'endpoint_secret': os.environ['STRIPE_ENDPOINT_SECRET']
}
stripe.api_key = stripe_keys['secret_key']
jwt = JWTManager(app)
async_mode = None
socket_ = SocketIO(app, async_mode=async_mode)
from app import routes