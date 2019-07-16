from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, validators


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(max=40, min=2)])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username', [validators.Length(max=40, min=2)])
    accept_tos = BooleanField('I accept the Terms of Service', [validators.InputRequired()])
    submit = SubmitField('Signup')
