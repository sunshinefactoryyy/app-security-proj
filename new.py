# from app import db
# from app.models import User
# db.create_all()
from werkzeug.serving import make_ssl_devcert 
make_ssl_devcert('./ssl', host='localhost')