#from crypt import methods
from fileinput import filename
from app.forms import EmployeeCreationForm, LoginForm, NewCatalogueItem, RegistrationForm, UpdateCatalogueItem, UpdateCustomerAccountForm, RequestResetForm, ResetPasswordForm, CustomerRequestForm, NewInventoryItem, UpdateEmployeeAccountForm, UpdateEmployeeManagementForm, UpdateInventoryItem , uploadfiles
from app.models import CatalogueProduct, Customer, Employee, Inventory, Request, Upload
from flask import render_template, url_for, flash, redirect, request, session, abort, jsonify, current_app , send_file
from io import BytesIO
from app import app, db, bcrypt, mail, stripe_keys
from app.train import *
from flask_login import login_user, current_user, logout_user, login_required
from requests.exceptions import HTTPError
import json
from app.utils import get_google_auth, generate_password, download_picture, save_picture, send_reset_email 
from app.config import Auth
from flask_mail import Message
from datetime import datetime
import os
import stripe
from app.train import bot
from functools import wraps
import xml.etree.ElementTree as ET
from lxml import etree
import shelve



# Public Routes
@app.route('/')
def home():
    procedure = [{
        'title': 'Request for repair',
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
        },]

    service = [{'service-title': 'Electronics Repairs',
                'service-desc': 'We offer repair services for computers, mobile phones, and more. Our repair process is entirely online, and you will receive constant updates on the status of your product! Prices range from $50-$3000 depending on the issue and the product.'
                },
                {'service-title': 'Two-way Delivery Service',
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
    collapse = [{'question': 'What services do you provide?',
                 'answer': 'We provide electronic repair services, two-way delivery services, computer diagnostics and many more! Head to our home page to find out.'
                },
                {'question': 'How do i contact Vision Core?',
                 'answer' : 'Apart from our hotline that is open during office hours, our website offers a chatbot that allows you to either chat with a bot online or with one of our customer service staff!',
                },
                {'question': 'What are the steps involved when i decide to repair with Vision Core?',
                 'answer': '1. Request for repair -> 2. Await for item status -> 3.Collect repair item.'
                },
                {'question': 'What are the payment methods accepted?',
                 'answer': 'We accept Paypal, Mastercard or your preferred bank app.'
                },
                {'question': 'How much is the two-way delivery fee?',
                 'answer': 'Two-way delivery fee has a $10 flat fee.'
                },
                {'question': 'What to do when i cannot drop off the product myself?',
                 'answer': 'No problem! Just engage our two-way delivery service that will deliver to and from your doorstep at any time slot you choose.'
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
        creation_time=datetime.utcnow().strftime(r'%Y-%m-%d %H:%M')
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password, picture='default.png', creation_datetime=creation_time)
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
        if Customer.query.filter_by(email=form.email.data).first():
            user = Customer.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for('customerAccount'))
            else:
                flash("Login unsuccessful. Please check email and password.", 'danger')
        elif Employee.query.filter_by(email=form.email.data).first():
            user = Employee.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('employeeInformation'))
            else:
                flash("Login unsuccessful. Please check email and password.", 'danger')

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
    path = 'static/src/profile_pics/'
    return render_template(
        'customer/account.html', 
        title='My Information', 
        navigation='Account',
        userData={
            'picture' : path+current_user.picture,
            'username' : current_user.username,
            'email' : current_user.email,
            'contact_no' : current_user.contact_no,
            'address' : current_user.address,
            'creation_datetime' : current_user.creation_datetime,
        }
    )

@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def editCustomerAccount():
    form = UpdateCustomerAccountForm()
    path = '/static/src/profile_pics/'
    
    if form.validate_on_submit():
        Customer.query.filter_by(email=form.email.data).first()
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if form.picture.data:
                picture_file = save_picture(form.picture.data, 'static/src/profile_pics')
                # os.remove(os.path.join(current_app.root_path,'static/src/profile_pics',current_user.picture))
                current_user.picture = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.contact_no = form.contact_no.data
            current_user.address = form.address.data
            current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash('Your account details have been updated!', 'success')
            redirect(url_for('customerAccount'))
        else:
            flash('Incorrect password.', 'danger')

    return render_template(
        'customer/editAccount.html', 
        title='My Information', 
        navigation='Account',
        username=current_user.username, 
        email=current_user.email, 
        form=form, 
        user=current_user,
        userData={
            'picture' : path+current_user.picture,
            'username' : current_user.username,
            'email' : current_user.email,
            'contact_no' : current_user.contact_no,
            'address' : current_user.address,
            'creation_datetime' : current_user.creation_datetime,
        }

    )

@app.route('/account/deactivate', methods=["GET", "POST"])
def deactivateAccount():
    if current_user.is_authenticated:
        if current_user.picture == 'default.png':
            pass
        else:
            os.remove(os.path.join('app/static/src/profile_pics/'+current_user.picture)) #deletes default.png
        deleted_user_id=current_user.id
        logout_user()
        Customer.query.filter_by(id=deleted_user_id).delete()
        db.session.commit()
        flash('Account has been successfully deleted!', 'success')
        return redirect(url_for('home'))
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('home'))

@app.route('/config')
def get_publishable_key():
    stripe_config = {'publicKey': stripe_keys['publishable_key']}
    return jsonify(stripe_config)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        redirect(url_for('home'))

    return "Success", 200

@app.route('/my-requests')
@login_required
def customerRequest():
    products = CatalogueProduct.query.all()
    form = CustomerRequestForm()
    requests = Request.query.filter_by(owner=current_user).order_by(Request.creation_datetime.desc())#.paginate(page=page, per_page=5)
    images = []
    for request_ in requests:
        paths = os.listdir(f'app/static/src/request_pics/{request_.images}')
        images.append(paths)
    return render_template(
        'customer/request.html', 
        title='Customer Request',
        navigation='Request', 
        # prodList=prodList, 
        requests=list(requests),
        images=images,
    )

@app.route('/my-requests/cart', methods=['GET', 'POST'])
@login_required
def customerCart():
    products = CatalogueProduct.query.all()
    img_path = '/static/src/product_pics/'
    prodList = [
        {'img': img_path + 'Gigabyte_X570_Aorus_Pro_Wifi.png', 'desc': 'Gigabyte X570 | Aorus Pro Wifi'},
        {'img': img_path + 'EVGA_GeForce_RTX_3080_Ti.png', 'desc': 'EVGA GeForce RTX | 3080 Ti'},
    ]
    for product in products:
        prodList.append({'img': img_path + product.productPicture, 'desc': product.productDescription})
    form = CustomerRequestForm()
    if form.validate_on_submit():
        image_folder = save_picture(form.images.data, path='static/src/request_pics', seperate=True)
        creation_time=datetime.utcnow().strftime(r'%Y-%m-%d %H:%M')
        new_request = Request(productName=form.productName.data,
                            images=image_folder, 
                            repairCost=300,
                            description=form.issueDesc.data, 
                            warranty=form.warranty.data,
                            owner=current_user,
                            creation_datetime=creation_time)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for("redirect_to_checkout"))
    return render_template('customer/cart.html', prodList=prodList, form=form)

@app.route('/my-requests/cart/checkout')
@login_required
def redirect_to_checkout():
    return render_template('customer/checkout.html')

@app.route('/my-requests/cart/checkout/new')
@login_required
def create_checkout_session():
    domain_url = "https://127.0.0.1:5000/my-requests/cart/checkout/"
    stripe.api_key = stripe_keys["secret_key"]
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "Flat Fee",
                    "quantity": 1,
                    "currency": "sgd",
                    "amount": "30000",
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/my-requests/cart/checkout/success')
@login_required
def checkout_success():
    flash(f"Your payment is successful!", "success")
    return redirect(url_for('customerRequest'))

@app.route('/my-requests/cart/checkout/cancelled')
@login_required
def checkout_cancelled():
    request = Request.query.filter_by(owner=current_user).order_by(Request.creation_datetime.desc()).first()
    db.session.delete(request)
    db.session.commit()
    flash(f"Your payment has been cancelled!", "danger")
    return redirect(url_for('customerCart'))

# Employee Routes
def authorised_only(f):
    @wraps(f)
    def decortated_function(*args, **kwargs):
        if Employee.query.filter_by(id=current_user.id).first() is None:
            return abort(403)
        return f(*args, **kwargs)
    return decortated_function

@app.route('/employee-information')
@login_required
@authorised_only
def employeeInformation():
    user = current_user

    return render_template(
        'employee/account/account.html', 
        title='Employee Account',
        user=user
    )

@app.route('/employee-information/edit', methods=["GET", "POST"])
@login_required
@authorised_only
def employeeInformationEdit():
    user = current_user
    form = UpdateEmployeeAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/src/profile_pics')
            # os.remove(part.picture.replace('static','app/static'))
            user.picture = picture_file
        user.email = form.email.data
        user.contact_no = form.contact.data
        user.address = form.address.data
        db.session.commit()
        return redirect(url_for('employeeInformation'))

    return render_template(
        'employee/account/accountEdit.html', 
        title='Edit Employee Account',
        user=user,
        form=form
    )

@app.route('/request-management')
@login_required
@authorised_only
def requestManagement():
    requestData = Request.query.all()
    return render_template(
        'employee/request/requestList.html', 
        title='Customer Requests',
        requestData=requestData,
    )

@app.route('/request-management/<int:requestID>')
@login_required
@authorised_only
def requestManagementDetails(requestID):
    request = Request.query.get_or_404(requestID)
    customer = Customer.query.filter_by(id=request.customerID).first()
    employee = Employee.query.filter_by(id=request.employeeID).first()

    return render_template(
        'employee/request/requestDetails.html', 
        title='Customer Requests',
        request=request,
        customer=customer,
        employee=employee
    )

@app.route('/catalogue', methods=["GET", "POST"])
@login_required
@authorised_only
def catalogue():
    form = NewCatalogueItem()
    catalogueData = CatalogueProduct.query.all()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/src/product_pics')
            product = CatalogueProduct(productPicture=picture_file, productName=form.name.data, productDescription=form.description.data, productCost=form.cost.data)
        else:
            product = CatalogueProduct(productName=form.name.data, productDescription=form.description.data, productCost=form.cost.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('catalogue'))

    return render_template(
        'employee/catalogue/catalogueList.html',
        title="Product Catalogue",
        catalogueData=catalogueData,
        form=form
    )

@app.route('/catalogue/<int:productID>')
@login_required
@authorised_only
def catalogueProduct(productID):
    product = CatalogueProduct.query.get_or_404(productID)

    return render_template(
        'employee/catalogue/catalogueProduct.html',
        title="Product Catalogue - " + product.productName,
        product=product,
    )

@app.route('/catalogue/<int:productID>/edit', methods=["GET", "POST"])
@login_required
@authorised_only
def catalogueProductEdit(productID):
    form = UpdateCatalogueItem()
    product = CatalogueProduct.query.get_or_404(productID)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/src/product_pics')
            # os.remove(product.picture.replace('static','app/static'))
            product.productPicture = picture_file
        product.productName = form.name.data
        product.productCost = form.cost.data
        if form.description.data:
            product.productDescription = form.description.data
        db.session.commit()
        return redirect(url_for('catalogueProduct', productID=productID))

    return render_template(
        'employee/catalogue/catalogueProductEdit.html',
        title="Edit Product - " + product.productName,
        product=product,
        form=form
    )

@app.route('/catalogue/<int:productID>/delete')
@login_required
@authorised_only
def catalogueProductDelete(productID):
    CatalogueProduct.query.filter_by(id=productID).delete()
    db.session.commit()
    return redirect(url_for('catalogue'))

@app.route('/inventory', methods=["GET", "POST"])
@login_required
@authorised_only
def inventoryManagement():
    form = NewInventoryItem()
    inventoryData = Inventory.query.all()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/src/part_pics')
            item = Inventory(partPicture=picture_file, partName=form.name.data, partDescription=form.description.data, partCost=form.cost.data, partQuantity=form.quantity.data)
        else:
            item = Inventory(partName=form.name.data, partDescription=form.description.data, partCost=form.cost.data, partQuantity=form.quantity.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('inventoryManagement'))

    return render_template(
        'employee/inventory/inventoryList.html',
        title='Inventory Management',
        inventoryData=inventoryData,
        form=form
    )

@app.route('/inventory/<int:partID>')
@login_required
@authorised_only
def inventoryPartDetails(partID):
    part = Inventory.query.get_or_404(partID)

    return render_template(
        'employee/inventory/inventoryDetails.html',
        title="Inventory - " + part.partName,
        part=part
    )

@app.route('/inventory/<int:partID>/edit', methods=["GET", "POST"])
@login_required
@authorised_only
def inventoryPartDetailsEdit(partID):
    form = UpdateInventoryItem()
    part = Inventory.query.get_or_404(partID)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/src/part_pics')
            # os.remove(part.picture.replace('static','app/static'))
            part.partPicture = picture_file
        part.partName = form.name.data
        part.partCost = form.cost.data
        if form.description.data:
            part.partDescription = form.description.data
        db.session.commit()
        return redirect(url_for('inventoryPartDetails', partID=partID))

    return render_template(
        'employee/inventory/inventoryDetailsEdit.html',
        title="Edit Inventory - " + part.partName,
        part=part,
        form=form
    )

@app.route('/inventory/<int:partID>/delete')
@login_required
@authorised_only
def inventoryPartDetailsDelete(partID):
    Inventory.query.filter_by(id=partID).delete()
    db.session.commit()

    return redirect(url_for('inventoryManagement'))

@app.route('/inventory/<int:partID>/replenish')
@login_required
@authorised_only
def inventoryPartDetailsReplenish(partID):
    Inventory.query.filter_by(id=partID).first().partQuantity += 10
    db.session.commit()

    return redirect(url_for('inventoryPartDetails', partID=partID))

@app.route('/employee-management', methods=["GET", "POST"])
@login_required
@authorised_only
def employeeManagement():
    employeeData = Employee.query.all()
    form = EmployeeCreationForm()
    creation_time=datetime.utcnow().strftime(r'%Y-%m-%d %H:%M')
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/src/profile_pics')
            employee = Employee(picture=picture_file, username=form.username.data, email=form.email.data, password=hashed_password, permissions=form.permissions.data,address=form.address.data,contact_no=form.contact.data,creation_datetime=creation_time)
        else:
            employee = Employee(username=form.username.data, email=form.email.data, password=hashed_password, permissions=form.permissions.data,address=form.address.data,contact_no=form.contact.data,creation_datetime=creation_time)
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('employeeManagement'))

    return render_template(
        'employee/employeeManagement/employeeList.html',
        title="Employee Management",
        employeeData=employeeData,
        form=form
    )

@app.route('/employee-management/<int:employeeID>')
@login_required
@authorised_only
def employeeManagementDetails(employeeID):
    employee = Employee.query.get_or_404(employeeID)

    return render_template(
        'employee/employeeManagement/employeeData.html',
        title="Employee Management - " + employee.username,
        employee=employee,
    )

@app.route('/employee-management/<int:employeeID>/edit', methods=["GET", "POST"])
@login_required
@authorised_only
def employeeManagementDetailsEdit(employeeID):
    employee = Employee.query.get_or_404(employeeID)
    form = UpdateEmployeeManagementForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/src/profile_pics')
            # os.remove(part.picture.replace('static','app/static'))
            employee.picture = picture_file
        employee.username = form.username.data
        if form.permissions.data:
            employee.permissions = form.permissions.data
        employee.email = form.email.data
        employee.contact_no = form.contact.data
        employee.address = form.address.data
        db.session.commit()
        return redirect(url_for('employeeManagementDetails', employeeID=employeeID))

    return render_template(
        'employee/employeeManagement/employeeDataEdit.html',
        title="Edit Employee Data - " + employee.username,
        employee=employee,
        user=current_user,
        form=form
    )


@app.route('/employee-management/<int:employeeID>/delete')
@login_required
@authorised_only
def employeeManagementDetailsDelete(employeeID):
    Employee.query.filter_by(id=employeeID).delete()
    db.session.commit()

    return redirect(url_for('employeeManagement'))


#Chatbot
@app.route('/chatbot', methods=['GET','POST'])
def chatbot():
    return render_template('public/newChat.html', title='Chat Support')

@app.route("/get", methods=['GET','POST'])
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))
#end Chatbot


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


@app.route('/upload-users', methods=['GET', 'POST'])
def upload():
    acctshelf = shelve.open("uploadacct",flag="c")
    uploadeduser = {}
    form = uploadfiles()
    i = 0
    error_check = False
    if request.method== 'POST':
        file = form.file.data
        if file == None:
            flash(f"No File Selected!", "danger")
        else:
            name = file.filename
            name = name.lower()
            if name.endswith(".xml"):
                # parse the xml file into the parser
                #parser = etree.XMLParser(load_dtd=True,no_network=False)
                try:
                    mytree = ET.parse(name)     #check for any DTD reference
                except ET.ParseError:
                    error_check = True

                if error_check == False:    # if there is no DTD reference
                    datas = mytree.getroot()
                    #return f'uploaded: {datas[0][0].text}'

                    # splitting the data up ( can as teacher if its better to hash the pasword first or what )
                    for i in range(len(datas)):
                        username = datas[i][0].text
                        email = datas[i][1].text
                        password = datas[i][2].text
                        #print(username) - for testing
                        #print(email)
                        #print(password)
                    
                    
                    #upload the user after parsing the data
                        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                        creation_time=datetime.utcnow().strftime(r'%Y-%m-%d %H:%M')
                        user = Customer(username=username, email=email, password=hashed_password, picture='default.png', creation_datetime=creation_time)
                        db.session.add(user)
                        db.session.commit()
                    
                        #uplaod to dict
                        uploadeduser[i] = {"username":username , "email":email}
                
                acctshelf["uploaded"] = uploadeduser
                acctshelf["errorcheck"] = error_check
                acctshelf.close()
                    
                """
                upload = Upload(filename = file.filename , data = file.read())
                db.session.add(upload)
                db.session.commit()
                return f'Uploaded: {file.filename}'
                """

                if error_check == False and len(uploadeduser) != 0:
                    flash(f"The accounts have been created! You may now use those account", "success")
        
                return redirect(url_for("uploadstatus")) 
            else:
                flash(f"Incorrect File Format", "danger")

    return render_template('customer/upload.html', title='Upload file', form = form )


@app.route('/uploadstatus')
def uploadstatus():
    db = shelve.open("uploadacct",flag="c")
    acctuploaded = db["uploaded"] # to retrieve teh list of accounts that have been added
    error_check = db["errorcheck"] # to show error msg for suspicious chracters
    if error_check == True:
        flash(f"XML File contains Inappropriate characters!", "danger")
        uploadeddict = {}
    elif len(acctuploaded) == 0:
        flash(f"No Account have been uploaded!", "danger")
        uploadeddict = {}
    else:
        uploadeddict = acctuploaded
        db["uploaded"] = {}
        db.close()
    return render_template('customer/uploadstatus.html', title='Uploaded Data', uploadeddict = uploadeddict , error_check = error_check)


@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename = upload.filename , as_attachment = True)

@app.route('/downloads/<upload_id>')
def downloads(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    name =upload.filename
    name =name.lower()
    if name.endswith(".xml"):
        parser = etree.XMLParser(load_dtd=True,no_network=False)
        mytree = ET.parse(name,parser=parser)
        return etree.dump(mytree.getroot())
    return f'Uploaded: {name}'
    #return send_file(BytesIO(upload.data), attachment_filename = upload.filename , as_attachment = True)