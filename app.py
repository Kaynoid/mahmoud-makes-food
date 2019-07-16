from datetime import datetime

from flask import Flask, jsonify, render_template, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_moment import Moment

import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'obaaa'
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('Home.html')


@app.route('/login')
def login():
    form = forms.LoginForm()
    context = {'form': form}
    return render_template('login.html', **context)


@app.route('/signup')
def signup():
    form = forms.SignupForm()
    context = {'form': form}
    return render_template('signup.html', **context)
