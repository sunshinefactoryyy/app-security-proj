# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# class Auth:
#     CLIENT_ID = '866787479507-n3f2q2kkcra67vls66q6hqmc8mjg2b18.apps.googleusercontent.com'
#     CLIENT_SECRET = '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'
#     REDIRECT_URL = 'https://127.0.0.1:5000/login/callback'
#     AUTH_URI = 'heept://accounts.google.com/o/oauth2/auth'
#     TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
#     USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    
# class Config:
#     APP_NAME = "Vision Core"
#     SECRET_KEY = os.environ.get('SECRET_KEY') or "somethingsecret"
    
# class DevConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")

# class ProdConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")