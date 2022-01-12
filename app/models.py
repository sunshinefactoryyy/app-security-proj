from sqlalchemy.orm import backref
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    inventory_posts = db.relationship('Inventory', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(20), nullable=False)
    productID = db.Column()


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String, unique=True, nullable=False)
    part_quantity = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    user = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    def __repr__(self):
        return f"Inventory('{self.part_name}', '{self.part_quantity}', '{self.user}', '{self.author_id}', '{self.date_posted}')"
