from datetime import datetime
import os

from flask import Flask, jsonify, render_template, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)


class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(10))

    def __reper__(self):
        return f'<User {self.username}'


@app.before_first_request
def before_first_request():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = forms.SignupForm()
    context = {'form': form}
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{user.username.capitalize()} your account was created successfully, welcome to your homepage')
        return redirect(url_for('home', name=user.username))
    return render_template('signup.html', **context)


@app.route('/login',methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    context = {'form': form}
    if form.validate_on_submit():
        user = User.query(username=form.username.data)
        return redirect(url_for('home', name=user.username))
    return render_template('login.html', **context)


@app.route('/home/<name>')
def home(name):
    context = {'name': name}
    return render_template('home.html', **context)