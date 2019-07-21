from datetime import datetime
import os
import datetime
from flask import Flask, jsonify, render_template, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


import forms, models

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
models.db.init_app(app)


@app.before_first_request
def before_first_request():
    models.db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = forms.SignupForm()
    context = {'form': form}
    if form.validate_on_submit():
        user = models.User(username=form.username.data, password=form.password.data)
        models.db.session.add(user)
        models.db.session.commit()
        flash(f'{user.username.capitalize()}, your account was created successfully, welcome to your homepage')
        return redirect(url_for('home', name=user.username))
    return render_template('signup.html', **context)


@app.route('/login',methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    context = {'form': form}
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if not user:
            flash('dumbfuck')
            return render_template('login.html', **context)
        elif user.is_admin == False:
            return redirect(url_for('home', name=user.username))
        elif user.is_admin == True:
            return redirect(url_for('admin_home', name=user.username))
    return render_template('login.html', **context)


@app.route('/home/<name>', methods=['GET', 'POST'])
def home(name):
    orderform = forms.OrderForm()
    orderform.item.choices = [(f.item, f.item) for f in models.Food.query.all()]
    context = {'name': name, 'orderform' : orderform}
    if orderform.validate_on_submit():
        order = models.Order(status='Order Received',date_in=datetime.datetime.now(),date_out=orderform.date.data,user=models.User.query.filter_by(username=name).first())
        models.db.session.add(order)
        models.db.session.commit()
    return render_template('home.html', **context)


@app.route('/admin/<name>', methods=['GET', 'POST'])
def admin_home(name):
    addform = forms.AdminAddForm()
    removeform = forms.AdminRemoveForm()
    removeform.item.choices = [(f.item, f.item) for f in models.Food.query.all()]
    context = {'name' : name, 'addform' : addform, 'removeform' : removeform}
    if addform.validate_on_submit():
        item = models.Food(item=addform.item.data, category=addform.category.data, price=addform.price.data)
        models.db.session.add(item)
        models.db.session.commit()
        flash(f'{item.item.capitalize()} was added succesfully', 'info')
        return redirect(url_for('admin_home', name=name))
    if removeform.validate_on_submit():
        item = models.Food.query.filter_by(item=removeform.item.data).first()
        models.db.session.delete(item)
        models.db.session.commit()
        return redirect(url_for('admin_home', name=name))
    return render_template('admin_home.html', **context)
