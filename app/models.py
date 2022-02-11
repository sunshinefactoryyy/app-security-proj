from enum import unique
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

class AccountCredentials(db.Model, UserMixin):
    __abstract__ = True
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profilePicutre = db.Column(db.String(120), unique=True)
    contactNumber = db.Column(db.Integer)
    password = db.Column(db.String(60), nullable=False)

class Customer(AccountCredentials):
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String(120))
    accountCreationDate = db.Column(db.Integer)
    requests = db.relationship('Request', backref='customer')

class Employee(AccountCredentials):
    id = db.Column(db.Integer, primary_key = True)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.id'))
    productName = db.Column(db.String(100), nullable=False)
    # productID = db.Column(db.Integer)
    # image = db.Column(db.)
    repairStatus = db.Column(db.String(20), nullable=False)
    repairCost = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(300), nullable=False)
    warranty = db.Column(db.Boolean, nullable=False)
    delivery = db.Column(db.Boolean, nullable=False)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    description = db.Column(db.String(420), nullable = False)
    quantity = db.Column(db.String(20), nullable = False)
