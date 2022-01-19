from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from app.forms import LoginForm, RegistrationForm, UpdateCustomerAccountForm
from app.models import User
from app.config import Auth
from flask_login import login_user, current_user, logout_user, login_required
from app.utils import get_google_auth
from requests.exceptions import HTTPError
import json

@app.route('/')
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
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, access=1)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to login.", "success")
        return redirect(url_for("login"))
    return render_template('register.html', title="Sign Up", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template('login.html', title='Login', form=form, auth_url=auth_url)

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
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.username = user_data['name']
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        return 'Could not fetch your information.'



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Customer Info', username=current_user.username, email=current_user.email)

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
    return render_template('editCustomerAccount.html', title='Customer Info', username=current_user.username, email=current_user.email, form=form, user=current_user)

@app.route('/account/deactivate', methods=["GET", "POST"])
def deactivateAccount():
    deleted_user_id=current_user.id
    logout_user()
    User.query.filter_by(id=deleted_user_id).delete()
    db.session.commit()
    flash('Account has been successfully deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/cusReq')
@login_required
def cusReq():
    return render_template('cusReq.html', title='Customer Request')

@app.route('/employeeInfo')
def employeeInfo():
    return render_template('employeeInfo.html', title='Employee Info')

@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(e):
    return render_template('errors/500.html'), 500

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

