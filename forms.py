from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, validators, PasswordField


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(max=15, min=4)],)
    password = PasswordField('Password', [validators.Length(min=5)])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username', [validators.Length(max=15, min=4)])
    password = PasswordField('Password', [validators.Length(max=20, min=5)])
    accept_tos = BooleanField('I accept the Terms of Service', [validators.InputRequired()])
    submit = SubmitField('Signup')


class DishForm(FlaskForm):
    dish_name = StringField('Main Dish', [validators.Length(min=2)])
    submit = SubmitField('Add Main Dish')


class SideForm(FlaskForm):
    side_dish_name = StringField('Side Dish', [validators.Length(min=2)])
    submit = SubmitField('Add Side Dish')


class DrinkForm(FlaskForm):
    drink_name = StringField('Drink', [validators.Length(min=2)])
    submit = SubmitField('Add Drink')
