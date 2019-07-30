from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields.html5 import DateTimeLocalField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=25, min=4), DataRequired(),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Username must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Length(min=5), DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=15, min=4)])
    password = PasswordField('Password', validators=[Length(max=20, min=5)])
    accept_tos = BooleanField('I accept the Terms of Service', validators=[DataRequired()])
    submit = SubmitField('Signup')


class AdminAddForm(FlaskForm):
    item = StringField('Item:', validators=[Length(min=2), DataRequired()])
    category = SelectField(f'Category: ', choices=[('Main Dish', 'Main Dish'), ('Side Dish', 'Side Dish'), ('Drink', 'Drink')])
    price = IntegerField('Price (EGP):', validators=[DataRequired()])
    add_submit = SubmitField('Add')


class AdminRemoveForm(FlaskForm):
    item = SelectField(f'Item:')
    remove_submit = SubmitField('Remove')


class OrderForm(FlaskForm):
    main = SelectField(f'Main:')
    side = SelectField(f'Side:')
    drink = SelectField(f'Drink:')
    date = DateTimeLocalField(f'Arrive at (mm/dd/YYYY hh:mm XM): ', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Order')


class MyOrdersForm(FlaskForm):
    item = SelectField(f'Orders:', choices=[('-','-')])
    option = SelectField(f'Action:', choices=[('Cancel Order','Cancel Order'), ('Check Status','Check Status')])
    submit = SubmitField('Proceed')


class ManageOrdersForm(FlaskForm):
    order = SelectField(f'Orders:',validators=[DataRequired()], choices=[('-','-')])
    option = SelectField('Action:',validators=[DataRequired()], choices=[('Remove Order','Remove Order'),('Set Status','Set Status')])
    status = SelectField('Status:',validators=[DataRequired()], choices=[('Order Received','Order Received'),('In Progress','In Progress'),('Delivered','Delivered')])
    manage_submit = SubmitField('Proceed')