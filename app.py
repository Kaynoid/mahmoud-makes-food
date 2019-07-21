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

from models import User, Dish, Side, Drink

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
        flash(f'{user.username.capitalize()}, your account was created successfully, welcome to your homepage')
        return redirect(url_for('home', name=user.username))
    return render_template('signup.html', **context)


@app.route('/login',methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    context = {'form': form}
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if not user:
            flash('dumbfuck')
            return render_template('login.html', **context)
        elif user.is_admin == False:
            return redirect(url_for('home', name=user.username))
        elif user.is_admin == True:
            return redirect(url_for('admin_home', name=user.username))
    return render_template('login.html', **context)


@app.route('/home/<name>')
def home(name):
    context = {'name': name}
    return render_template('home.html', **context)


@app.route('/admin/<name>', methods=['GET', 'POST'])
def admin_home(name):
    dish = forms.DishForm()
    side = forms.SideForm()
    drink = forms.DrinkForm()
    context = {'name' : name, 'dish' : dish, 'side' : side, 'drink' : drink}
    if dish.validate_on_submit():
        meal = Dish(dish=dish.dish_name.data)
        db.session.add(meal)
        db.session.commit()
        flash(f'{meal.dish.capitalize()} was added succesfully')
    if side.validate_on_submit():
        meal = Side(side=side.side_dish_name.data)
        db.session.add(meal)
        db.session.commit()
        flash(f'{meal.side.capitalize()} was added succesfully')
    if drink.validate_on_submit():
        meal = Drink(drink=drink.drink_name.data)
        db.session.add(meal)
        db.session.commit()
        flash(f'{meal.drink.capitalize()} was added succesfully')
    return render_template('admin_home.html', **context)
