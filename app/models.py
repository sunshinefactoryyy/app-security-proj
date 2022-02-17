from app import db, login_manager, app
from app.customMixin import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    if Customer.query.filter_by(username=user_id).first():
        return Customer.query.filter_by(username=user_id).first()
    elif Employee.query.filter_by(username=user_id).first():
        return Employee.query.filter_by(username=user_id).first()

ACCESS = {'customer': 1,
          'admin': 2}

class AccountCredentials(db.Model, UserMixin):
    __abstract__ = True
    creation_datetime = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False) # String should be cap 20
    picture = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact_no = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(200))
    password = db.Column(db.String(60), nullable=False)
    tokens = db.Column(db.Text)


class Customer(AccountCredentials):
    id = db.Column(db.Integer, primary_key = True)
    requests = db.relationship('Request', backref='owner', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Customer.query.get(user_id)

class Employee(AccountCredentials):
    id = db.Column(db.Integer, primary_key = True)
    permissions = db.Column(db.Integer, nullable=False)

class Request(db.Model):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    creation_datetime = db.Column(db.String(20), nullable=False)
    productName = db.Column(db.String(100), nullable=False)
    images = db.Column(db.String(100), nullable=False)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    employeeID = db.Column(db.Integer, db.ForeignKey('employee.id'))
    repairStatus = db.Column(db.Integer, nullable=False, default=0)
    repairCost = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(300), nullable=False)
    warranty = db.Column(db.Integer, nullable=False)

    # productID = db.Column()


class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    partPicture = db.Column(db.String(200))
    partName = db.Column(db.String(100), nullable=False)
    partDescription = db.Column(db.String(1000), nullable=False)
    partCost = db.Column(db.Float, nullable=False)
    partQuantity = db.Column(db.Integer, nullable=False)

class CatalogueProduct(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    productPicture = db.Column(db.String(200))
    productName = db.Column(db.String(200), nullable=False)
    productDescription = db.Column(db.String(1000), nullable=False)
    productCost = db.Column(db.Float, nullable=False)
