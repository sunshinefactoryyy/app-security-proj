from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from data.forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab2d494b73d4d8ee5ef8f28b5d575bcd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}'"


@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
  
@app.route('/cusInfo')
def cusInfo():
    return render_template('cus_info.html', title='Customer Info')

@app.route('/cusReq')
def cusReq():
    return render_template('cusReq.html', title='Customer Request')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response
    
if __name__ == '__main__':
    app.run(debug=True)
