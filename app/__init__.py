from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY'],
    'endpoint_secret': os.environ['STRIPE_ENDPOINT_SECRET']
}
stripe.api_key = stripe_keys['secret_key']
async_mode = None
socket_ = SocketIO(app, async_mode=async_mode)
from app import routes