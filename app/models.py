from re import U
from sqlalchemy.orm import backref
from app import db, login_manager
from flask_login import UserMixin
from datetime import date, datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # inventory_posts = db.relationship('Inventory', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# class Request(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     productName = db.Column(db.String(20), nullable=False)
#     productID = db.Column()


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String, unique=True, nullable=False)
    part_quantity = db.Column(db.Integer, nullable=False)
    part_cost = db.Column(db.Integer, unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    user = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    def __repr__(self):
        return f"Inventory('{self.part_name}', '{self.part_quantity}', '{self.user}', '{self.user_id}', '{self.date_posted}')"

    def __init__(self, part_name, part_quantity, part_cost, date_posted, user, user_id):
        self.part_name = part_name
        self.part_quantity = part_quantity
        self.part_cost = part_cost
        self.date_posted = date_posted
        self.user = user
        self.user_id = user_id
    
    def create(self):
        part_name = open('part_name.txt', 'w')
        part_name_content = part_name.create()
        part_name.close()

        part_quantity = open('part_quantity.txt', 'w')
        part_quantity_content = part_quantity.create()
        part_quantity.close()

    def update(self):
        part_name = open('part_name.txt', 'u')
        part_name_update = part_name.update()
        part_name.close()

        part_quantity = open('part_quantity.txt', 'u')
        part_quantity_update = part_name.update()
        part_quantity.close()

    def read(self):
        part_name = open('part_name.txt', 'r')
        part_name_content = part_name.read()
        part_name.close()

    def delete(self):
        part_name = open('part_name.txt', 'd')
        part_name_delete = part_name.delete()
        part_name.close()

    

