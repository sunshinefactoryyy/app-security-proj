from requests_oauthlib import OAuth2Session
from app.config import Auth
import string
import secrets
import urllib.request
import os
from PIL import Image
from flask import current_app, url_for

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
    output_size = (250,250)
    i = Image.open(fp)
    i.thumbnail(output_size)
    i.save(fp)
    return url_for('static', filename=f'src/profile_pics/{fn}.jpeg')