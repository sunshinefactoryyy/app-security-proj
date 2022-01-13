from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import LoginForm, RegistrationForm, UpdateCustomerAccountForm
from app.models import Customer
from flask_login import login_user, current_user, logout_user, login_required

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
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to login.", "success")
        return redirect(url_for("login"))
    return render_template('register.html', title="Sign Up", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
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
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Your account details have been updated!', 'success')
        redirect(url_for('account'))
    return render_template('editCustomerAccount.html', title='Customer Info', username=current_user.username, email=current_user.email, form=form)

@app.route('/account/deactivate')
def deactivateAccount():
    deleted_user_id=current_user.id
    logout_user()
    Customer.query.filter_by(id=deleted_user_id).delete()
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

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

