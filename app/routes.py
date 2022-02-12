from flask import render_template, url_for, flash, redirect, request, session, abort
from app import app, db, bcrypt, mail
from app.forms import LoginForm, RegistrationForm, UpdateCustomerAccountForm, RequestResetForm, ResetPasswordForm, inventoryForm, CustomerRequestForm, NewInventoryItem
from app.models import Customer, Inventory
from flask_login import login_user, current_user, logout_user, login_required
from requests.exceptions import HTTPError
import json
from app.utils import get_google_auth, generate_password, download_picture, save_picture
from app.config import Auth
from flask_mail import Message
import os



# Public Routes
@app.route('/')
def home():
    procedure = [{'title': 'Request for repair',
                  'icon': "bi bi-tools",
                  'desc': 'Sign up for a free account on our website. You can either pay the stated flat price, or request for a quote with our free diagnostics. All payments are done online. Either physically drop off your item, or use our 2-way delivery service & await the status of your item.'
                  },
                  {'title': 'Await for item status',
                  'icon': "bi bi-clipboard-check",
                  'desc': 'Check your account on this website for constant updates on your item. You may also choose your preferred mode of communication. If needed, you can interact with our chatbot or call our hotline (+65 9812 3456).'
                  },
                  {'title': 'Collect repaired item',
                  'icon': "bi bi-truck",
                  'desc': 'After your item has been repaired, you can physically collect it or via delivery to your house.'
                  },
            ]

    service = [{'service-title': 'Electronics Repairs',
                'service-desc': 'We offer repair services for computers, mobile phones, and more. Our repair process is entirely online, and you will receive constant updates on the status of your product! Prices range from $50-$3000 depending on the issue and the product.'
                },
                {'service-title': '2-way Delivery Service',
                'service-desc': 'No time to drop in personally with your computer? No problem! Just engage our two-way delivery service that will deliver to and from your doorstep at any time slot you choose.'
                },
                {'service-title': 'Computer Diagnostics',
                'service-desc': 'Before we give you a quote for your repair, our company offers a free computer diagnosis for all customers regardless of whether you decide to proceed with the repair or not! This is only applicable if you request for a quote.',
                },
                {'service-title': 'Contact Us',
                'service-desc': 'Apart from our hotline that is open during office hours, our website offers a chatbot that allows you to either chat with a bot online or with one of our customer service staff!'
                }          
            ]

    return render_template(
        'public/home.html', 
        title='Home',
        procedure = procedure,
        service = service
    )

@app.route('/about')
def about():
    return render_template(
        'public/about.html', 
        title='About Us'
    )

@app.route('/faq')
def faq():
    collapse = [{'question': 'Question 1',
                'answer': 'Answer 1'
                },
                {'question': 'Question 2',
                    'answer': 'Answer 2'
                },
                {'question': 'Question 3',
                    'answer': 'Answer 3'
                }
            ]
    return render_template(
        'public/faq.html', 
        title='FAQ',
        collapse = collapse
    )



# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customerRequest'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash(f"Your account has been created! You are now logged in!", "success")
        return redirect(url_for("customerRequest"))

    return render_template(
        'authentication/register.html', 
        title="Sign Up", 
        form=form
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('customerAccount'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('customerAccount'))
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
            user.picture = download_picture(user_data['picture'])
            user.password = bcrypt.generate_password_hash(generate_password()).decode('utf-8')
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        return 'Could not fetch your information.'

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='213587x@gmail.com', recipients=[user.email])
    msg.body = f"To reset your password, visit the following link:\n{url_for('reset_token', token=token, _external=True)}\nIf you did not make this request then simply ignore this email and no changes will be made."
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for('home'))
    return render_template('authentication/reset_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Customer.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expires token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated! You are now able to login.", "success")
        return redirect(url_for("login"))

    return render_template('authentication/reset_token.html', title='Reset Password', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



# Customer Routes
@app.route('/account')
@login_required
def customerAccount():
    form = UpdateCustomerAccountForm()
    return render_template(
        'customer/account.html', 
        title='My Information', 
        navigation='Account',
        userData={
            'picture' : current_user.picture,
            'username' : current_user.username,
            'email' : current_user.email,
            'contact_no' : current_user.contact_no,
            'address' : current_user.address,
            'creation_datetime' : current_user.creation_datetime.strftime(r'%Y-%m-%d %H:%M'),
        }
    )

@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def editCustomerAccount():
    form = UpdateCustomerAccountForm()
    user = current_user
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            os.remove(current_user.picture.replace('/static','app/static'))
            current_user.picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.contact_no = form.contact_no.data
        current_user.address = form.address.data
        current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        flash('Your account details have been updated!', 'success')
        redirect(url_for('customerAccount'))

    return render_template(
        'customer/editAccount.html', 
        title='My Information', 
        navigation='Account',
        username=current_user.username, 
        email=current_user.email, 
        form=form, 
        user=current_user,
        userData={
            'picture' : current_user.picture,
            'username' : current_user.username,
            'email' : current_user.email,
            'contact_no' : current_user.contact_no,
            'address' : current_user.address,
            'creation_datetime' : current_user.creation_datetime.strftime(r'%Y-%m-%d %H:%M'),
        }

    )

@app.route('/account/deactivate', methods=["GET", "POST"])
def deactivateAccount():
    os.remove(current_user.picture.replace('/static','app/static'))
    deleted_user_id=current_user.id
    logout_user()
    Customer.query.filter_by(id=deleted_user_id).delete()
    db.session.commit()
    flash('Account has been successfully deleted!', 'success')
    return redirect(url_for('home'))

img_path = '../static/public/'
prodList = [
    {'img': img_path + 'Gigabyte_X570_Aorus_Pro_Wifi.png', 'name': 'Gigabyte X570 | Aorus Pro Wifi', 'desc': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
    {'img': img_path + 'EVGA_GeForce_RTX_3080_Ti.png', 'name': 'EVGA GeForce RTX | 3080 Ti', 'desc': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
    {'img': img_path + 'Gigabyte_X570_Aorus_Pro_Wifi.png', 'name': 'Gigabyte X570 | Aorus Pro Wifi', 'desc': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
    {'img': img_path + 'EVGA_GeForce_RTX_3080_Ti.png', 'name': 'EVGA GeForce RTX | 3080 Ti', 'desc': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
]

@app.route('/my-requests')
@login_required
def customerRequest():
    form = CustomerRequestForm()
    return render_template(
        'customer/request.html', 
        title='Customer Request',
        navigation='Request', 
        prodList = prodList, 
        form=form
    )

@app.route('/my-requests/cart')
@login_required
def customerCart():
    form = CustomerRequestForm()
    return render_template('customer/cart.html', prodList=prodList, form=form)

# Employee Routes
@app.route('/employee-information')
def employeeInformation():
    return render_template(
        'employee/account.html', 
        title='Employee Account'
    )

@app.route('/request-management')
def requestManagement():
    return render_template(
        'employee/request.html', 
        title='Customer Requests'
    )

@app.route('/inventory')
def inventoryManagement():
    form = NewInventoryItem()
    if form.validate_on_submit():
        item = Inventory(name=form.name.data, descriprion=form.description.data, quantity=form.quantity.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('inventoryManagement'))

    return render_template(
        'employee/inventory.html',
        title='Inventory Management',
        form=form
    )


#Chatbot
@app.route('/chat')
def chatbot():
    return render_template("chat.html")

# @app.route("/get")
# def get_chat_response():
#     userText = request.args.get('msg')
#     return str(bot.get_response(userText))



@app.route('/inventory')
@login_required
def inventory():
    return render_template(
        'inventory.html', 
        title='Inventory'
        )

@app.route('/inventory/new', methods=['GET', 'POST'])
@login_required
def new_part():
    form = inventoryForm()
    if form.validate_on_submit():
        new = Inventory(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new)
        db.session.commit()
        redirect(url_for('inventory'))
    return render_template(
        'newPart.html', 
        title='New Part', 
        form=form, 
        legend='New Part'
        )

# @app.route('/inventory/<int:part_id>')
# def part(part_id):
#     part = Inventory.query.get_or_404(part_id)
#     return render_template('part.html', title=part.title, part=part)

@app.route('/inventory/<int:part_id>/update', methods=['GET', 'POST'])
@login_required
def update_part(part_id):
    part = Inventory.query.get_or_404(part_id)
    if part.author != current_user:
        abort(403)
    form = inventoryForm()
    if form.validate_on_submit():
        part.title = form.title.data
        part.content = form.content.data
        db.session.commit()
        flash('The part has been updated.', 'success')
        redirect(url_for(
            'part',
            part_id=part.id
            )
        )
    
    elif request.method == 'GET':
        form.title.data = part.title
        form.content.data = part.content
    return render_template(
        'newPart.html',
        title='Update Part',
        form=form,
        legend='Update Part'
        )
    
@app.route('/inventory/<int:part_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_part(part_id):
    part = Inventory.query.get_or_404(part_id)
    if part.author != current_user:
        abort(403)
    db.session.delete(part)
    db.session.commit()
    flash('The part has been deleted.', 'success')
    redirect(url_for(
        'inventory.html'
        ))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Customer Info', username=current_user.username, email=current_user.email)


# Error Handling
@app.errorhandler(404)
def notFound():
    return render_template(
        '404.html', 
        title='404 - Page not found'
    )

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

# Clear Cache
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response
