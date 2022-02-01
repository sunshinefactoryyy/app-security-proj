from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from app.forms import LoginForm, RegistrationForm, UpdateCustomerAccountForm
from app.models import Customer
from flask_login import login_user, current_user, logout_user, login_required
from requests.exceptions import HTTPError
import json
from app.utils import get_google_auth, generate_password
from app.config import Auth




# Public Routes
@app.route('/')
def home():
    return render_template(
        'public/home.html', 
        title='Home'
    )

@app.route('/about')
def about():
    return render_template(
        'public/about.html', 
        title='About Us'
    )

@app.route('/faq')
def faq():
    return render_template(
        'public/faq.html', 
        title='FAQ'
    )



# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f"Your account has been created! You are now logged in!", "success")
        return redirect(url_for("account"))

    return render_template(
        'authentication/register.html', 
        title="Sign Up", 
        form=form
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template(
        'authentication/login.html', 
        title='Login', 
        form=form,
        auth_url=auth_url
    )


@app.route('/login/callback')
def callback():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('home'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = get_google_auth(state=session.get('oauth_state'))
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = Customer.query.filter_by(email=email).first()
            if user is None:
                user = Customer()
                user.email = email
            user.username = user_data['name']
            user.tokens = json.dumps(token)
            user.picture = user_data['picture']
            user.password = bcrypt.generate_password_hash(generate_password()).decode('utf-8')
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        return 'Could not fetch your information.'



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



# Customer Routes
@app.route('/account')
@login_required
def customerAccount():
    return render_template(
        'customer/account.html', 
        title='Customer Info', 
        navigation='Account',
        username=current_user.username, 
        email=current_user.email
    )

@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def editCustomerAccount():
    form = UpdateCustomerAccountForm()
    user = current_user
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Your account details have been updated!', 'success')
        redirect(url_for('account'))

    return render_template(
        'customer/editAccount.html', 
        title='Customer Info', 
        navigation='Account',
        username=current_user.username, 
        email=current_user.email, 
        form=form, 
        user=current_user
    )

@app.route('/account/deactivate')
def deactivateAccount():
    Customer.query.filter_by(id=current_user.id).delete()
    db.session.commit()
    logout_user()
    flash('Account has been successfully deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/cusReq')
@login_required
def customerRequest():
    return render_template(
        'customer/request.html', 
        title='Customer Request',
        navigation='Request'
    )



# Employee Routes
@app.route('/employeeInfo')
def employeeInfo():
    return render_template(
        'employee/account.html', 
        title='Employee Info'
    )



# Error Handling
@app.errorhandler(404)
def notFound():
    return render_template(
        '404.html', 
        title='404 - Page not found'
    )



# Clear Cache
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

