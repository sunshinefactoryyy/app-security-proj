class Auth:
    CLIENT_ID = '866787479507-n3f2q2kkcra67vls66q6hqmc8mjg2b18.apps.googleusercontent.com'
    CLIENT_SECRET = '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'
    REDIRECT_URI = 'https://127.0.0.1:5000/login/callback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email']