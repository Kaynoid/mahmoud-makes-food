from datetime import datetime

from flask import Flask, jsonify, render_template, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_moment import Moment

import forms
import models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'obaaa'
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.before_first_request
def before_first_request():
    models.db.create_tables([models.User], safe=True)
    models.db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = forms.SignupForm()
    context = {'form': form}
    if form.validate_on_submit():
        user = models.User.create(username=form.username.data, password=form.password.data)
        flash(f'{user.username.capitalize()} your account was created successfully, welcome to your homepage')
        return redirect(url_for('home',name = user.username))
    return render_template('signup.html', **context)


@app.route('/login',methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    context = {'form': form}
    if form.validate_on_submit():
        user = models.User.get(username=form.username.data, password=form.password.data)
        return redirect(url_for('home', name=user.username))
    return render_template('login.html', **context)


@app.route('/home/<name>')
def home(name):
    context = {'name': name}
    return render_template('home.html', **context)