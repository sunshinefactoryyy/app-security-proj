from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, validators, MultipleFileField, RadioField, FloatField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import Customer, Employee
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
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
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

class EmployeeCreationForm(FlaskForm):
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    permissions = RadioField("Employee Permission", choices=[(1, "Super Administrator"), (2, 'Employee')], validators=[DataRequired()])
    address = StringField("Residential Address", validators=[DataRequired()])
    contact = IntegerField("Contact Number", validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_username(self, username):
        user = Employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")

class UpdateEmployeeManagementForm(FlaskForm):
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    permissions = RadioField("Employee Permissions", choices=[(1, "Super Administrator"), (2, 'Employee')])
    address = StringField("Residential Address", validators=[DataRequired()])
    contact = IntegerField("Contact Number", validators=[DataRequired()])
    submit = SubmitField("Update")

class UpdateEmployeeAccountForm(FlaskForm):
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    email = StringField("Email Address", validators=[DataRequired(), Email(message='Invalid email')])
    address = StringField("Residential Address", validators=[DataRequired()])
    contact = IntegerField("Contact Number", validators=[DataRequired()])
    submit = SubmitField("Update")

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
    productName = StringField("Select Product", validators=[DataRequired()])
    images = MultipleFileField('Upload Images', validators=[FileAllowed(['jpg', 'png', 'jpeg','pdf'])])
    issueDesc = TextAreaField('Issue Description', validators=[Length(max=200), DataRequired()])
    warranty = RadioField('Warranty Status', validators=[DataRequired()], choices=[(1, 'Active'), (0, 'Expired')], default='')
    price = RadioField('Price', validators=[DataRequired()], choices = [(300,'S$300'), (0,'Get Quote')], default='')
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
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    name = StringField("Part Name", validators=[DataRequired()])
    description = TextAreaField("Part Description", validators=[DataRequired()])
    cost = FloatField("Part Cost", validators=[DataRequired()])
    quantity = IntegerField("Part Quantity", validators=[DataRequired()])
    submit = SubmitField("Add Part")

class UpdateInventoryItem(FlaskForm):
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    name = StringField("Part Name", validators=[DataRequired()])
    cost = FloatField("Part Cost", validators=[DataRequired()])
    description = TextAreaField("Part Description")
    submit = SubmitField("Update")

class NewCatalogueItem(FlaskForm):
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    name = StringField("Product Name", validators=[DataRequired()])
    cost = FloatField("Product Cost", validators=[DataRequired()])
    description = TextAreaField("Product Description", validators=[DataRequired()])
    submit = SubmitField("Add Product")

class UpdateCatalogueItem(FlaskForm):
    picture = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    name = StringField("Product Name", validators=[DataRequired()])
    cost = FloatField("Product Cost", validators=[DataRequired()])
    description = TextAreaField("Product Description")
    submit = SubmitField("Update")

class OTPForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired()])
    submit = SubmitField('Verify')

class SecurityQuestionsForm(FlaskForm):
    question = RadioField('Which is the correct option', choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], validators=[DataRequired()])
    submit = SubmitField('Verify')

class Set2FAForm(FlaskForm):
    choose = RadioField('Preferred Authentication Method', choices=[('otp', 'OTPs through Email'), ('sQn', 'Pre-set Security Questions')], validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SetSecurityQuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    correct = SelectField('Correct Option', choices=[(1, 'First'), (2, 'Second'), (3, 'Third')], validators=[DataRequired()])
    submit = SubmitField('Confirm')