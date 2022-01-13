from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    terms_and_conditions = BooleanField("I agree to the Terms & Conditions")
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class UpdateCustomerAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")

class inventoryForm(FlaskForm):
    username = StringField("User", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=20)])
    part_name = StringField("Part Name", validators=[DataRequired()])
    part_quantity = IntegerField("Part Quantity", validators=[DataRequired()])
    part_cost = IntegerField("Part Cost", validators=[DataRequired()])
    date_posted = DateField("Date Posted", validators=[DataRequired()])

    def validate_part_quantity(self, part_quantity):
        try:
            type(part_quantity)
        except ValueError:
            print("Sorry, please enter a number.")

    def validate_part_cost(self, part_cost):
        try:
            type(part_cost)
        except ValueError:
            print("Sorry, please enter a number.")
    
class updateInventoryForm(FlaskForm):
    part_name = StringField("Part Name", validators=[DataRequired()])
    part_quantity = IntegerField("Part Quantity", validators=[DataRequired()])
    part_cost = IntegerField("Part Cost", validators=[DataRequired()])
    date_posted = DateField("Date Posted", validators=[DataRequired()])
    
    def validate_part_quantity(self, part_quantity):
        if (part_quantity.data < 50) or part_quantity.data == 0:
            try:
                type(part_quantity)
            except ValueError:
                print("Sorry, please enter a number.")
            
        else:
            print("This part is still in stock. There is no need to restock.")
    