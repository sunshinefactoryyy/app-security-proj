from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, validators, MultipleFileField, RadioField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import Customer, Employee, User
import phonenumbers

class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    terms_and_conditions = BooleanField("I agree to the Terms & Conditions", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        user = Customer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class UpdateCustomerAccountForm(FlaskForm):
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png'])])
    username = StringField("Username:", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address:", validators=[DataRequired(), Email(message='Invalid email')])
    contact_no = StringField("Contact number:", validators=[DataRequired(), Length(min=8, max=20)])
    address = StringField("Address:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Customer.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Customer.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")
        
    def validate_phone_no(self, phone_no):
        if phone_no.data != current_user.phone_no:
            user = Customer.query.filter_by(phone_no=phone_no.data).first()
            if user:
                raise ValidationError("That phone number is taken. Please choose a different one.")
            else:
                try:
                    input_number = phonenumbers.parse(phone_no.data)
                    if not phonenumbers.is_valid_number(input_number):
                        raise ValidationError("Invalid phone number.")
                except:
                    input_number = phonenumbers.parse(f"+65{phone_no.data}")
                    if not (phonenumbers.is_valid_number(input_number)):
                        raise ValidationError("Invalid phone number.")
        
    
    

class inventoryForm(FlaskForm):
    username = StringField("User", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=20)])
    part_name = StringField("Part Name", validators=[DataRequired()])
    part_quantity = IntegerField("Part Quantity", validators=[DataRequired()])
    part_cost = IntegerField("Part Cost", validators=[DataRequired()])
    date_posted = DateField("Date Posted", validators=[DataRequired()])
    add = SubmitField("Add Part")

    def validate_part_quantity(self, part_quantity):
        try:
            type(part_quantity)

            if part_quantity <= 0:
                raise ValidationError("Part quantity cannot be 0. Please try again.")
            
        except ValueError:
            raise ValidationError("Please enter a number.")

    def validate_part_cost(self, part_cost):
        try:
            type(part_cost)
            if part_cost <= 0:
                raise ValidationError("Please enter a valid cost")

        except ValueError:
            raise ValidationError("Please enter a number.")
    
class updateInventoryForm(FlaskForm):
    part_name = StringField("Part Name", validators=[DataRequired()])
    part_quantity = IntegerField("Part Quantity", validators=[DataRequired()])
    part_cost = IntegerField("Part Cost", validators=[DataRequired()])
    date_posted = DateField("Date Posted", validators=[DataRequired()])
    update = SubmitField("Update")
    
    def validate_part_quantity(self, part_quantity):
        if (part_quantity.data < 50) or part_quantity.data == 0:
            try:
                type(part_quantity)
                if part_quantity <= 0:
                    raise ValidationError("Please enter a valid cost")

            except ValueError:
                raise ValidationError("Please enter a number.")
            
        else:
            raise Exception("This part is still in stock. No need to restock.")

class EmployeeCreationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    def validate_username(self, username):
        user = Employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class UpdateEmployeeCreationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Employee.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Employee.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")

class CustomerRequestForm(FlaskForm):
    productName = SelectField("Select Product", [validators.DataRequired()], choices = [('123','Gigabyte X570 | Aorus Pro Wifi'),('321', 'Gigabyte X570 | Aorus Pro Wifi')], default='')
    images = MultipleFileField('Upload Images', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg','pdf'], 'Images only')])
    issueDesc = TextAreaField('Issue Description', [validators.length(max=200), validators.DataRequired()])
    warranty = RadioField('Warranty Status', [validators.DataRequired()], choices=[('1', 'Active'), ('0', 'Expired')], default='')
    price = RadioField('Price', [validators.DataRequired()], choices = [('1','S$300'),('0', 'Get A Quote')], default='')

    delivery = SelectField('Doorstep Delivery', [validators.DataRequired()], choices = [('1','10.00'),('2', 'No')], default='')
    submit = SubmitField('Confirm Order')

class RequestResetForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    def validate_email(self, email):
        user = Customer.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")

class NewInventoryItem(FlaskForm):
    name = StringField("Part Name", validators=[DataRequired()])
    description = TextAreaField("Part Description", validators=[DataRequired()])
    quantity = StringField("Quantity", validators=[DataRequired()])
    submit = SubmitField('Add Part')
