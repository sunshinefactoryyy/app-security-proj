from flask import render_template, url_for, flash, redirect
from data import app, db, bcrypt
from data.forms import LoginForm, RegistrationForm
from data.models import User

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to login.", "success")
        return redirect(url_for("login"))
    return render_template('register.html', title="Sign Up", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "lgf2111@gmail.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
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

