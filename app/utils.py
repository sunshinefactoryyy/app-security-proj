from requests_oauthlib import OAuth2Session
from app.config import Auth
import string
import secrets
import urllib.request
import os
from PIL import Image
from flask import current_app, url_for
from pathlib import Path
from flask_mail import Message
from app import mail

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='213587x@gmail.com', recipients=[user.email])
    msg.body = f"To reset your password, visit the following link:\n{url_for('reset_token', token=token, _external=True)}\nIf you did not make this request then simply ignore this email and no changes will be made."
    mail.send(msg)

def generate_password():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password

def download_picture(pic_url):
    while True:
        fn = secrets.token_hex(8)
        fp = f'{current_app.root_path}/static/src/profile_pics/{fn}.jpeg'
        if not os.path.exists(fp):
            with open(fp, 'w'): pass
            break
    urllib.request.urlretrieve(pic_url, fp)
    i = Image.open(fp)
    i.save(fp)
    return f'{fn}.jpeg'

def save_picture(form_picture, path, seperate=False):
    if seperate:
        form_pictures = form_picture
        folder_fn = secrets.token_hex(8)
        folder_path = os.path.join(current_app.root_path, Path(path), folder_fn)
        os.mkdir(folder_path)
        for form_picture in form_pictures:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form_picture.filename)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(folder_path, picture_fn)
            output_size = (256, 256)
            i = Image.open(form_picture)
            i.thumbnail(output_size)
            i.save(picture_path)
        return folder_fn
    else:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, Path(path), picture_fn)
        output_size = (256, 256)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

    return picture_fn