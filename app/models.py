from app import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

ACCESS = {'customer': 1,
          'admin': 2}

class AccountCredentials(db.Model, UserMixin):
    __abstract__ = True
    # username = db.Column(db.String(20), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    # password = db.Column(db.String(60), nullable=False)
    
    # id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    username = db.Column(db.String(20), unique=True, nullable=False) # String should be cap 20
    picture = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_no = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(200))
    password = db.Column(db.String(60), nullable=False)
    tokens = db.Column(db.Text)


class Customer(AccountCredentials):
    id = db.Column(db.Integer, primary_key = True)

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


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(20), nullable=False)
    # productID = db.Column()


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    productID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customer.id'))
    productName = db.Column(db.String(100), nullable=False)
    # productID = db.Column(db.Integer)
    # image = db.Column(db.)
    repairStatus = db.Column(db.String(20), nullable=False)
    repairCost = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(300), nullable=False)
    warranty = db.Column(db.Boolean, nullable=False)
    delivery = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Inventory('{self.part_name}', '{self.part_quantity}' '{self.part_cost}', '{self.date_posted}')"

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    access = db.Column(db.Integer, nullable=False, default=1)
    username = db.Column(db.String(100), unique=True, nullable=False) # String should be cap 20
    avatar = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    tokens = db.Column(db.Text)
    
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
        return User.query.get(user_id)
    
    def is_admin(self):
        return True if self.access == ACCESS['admin'] else False
    def access_level(self, access):
        return True if self.access <= access else False
    def __repr__(self):
        role = dict((v, k) for k, v in ACCESS.items())[self.access].capitalize()
        return f"{role}('{self.username}', '{self.email}', '{self.password}')"

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    description = db.Column(db.String(420), nullable = False)
    quantity = db.Column(db.String(20), nullable = False)
