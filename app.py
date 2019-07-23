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
    myorderform = forms.MyOrdersForm()
    user_id =  models.User.query.filter_by(username=name).first().id
    user_orders = models.Order.query.filter_by(user_id=user_id)
    order_id = [o.id for o in user_orders]
    log = models.OrderFoodLog.query.filter(models.OrderFoodLog.order_id.in_(order_id))
    myorderform.item.choices = [(o.id , o.food.item) for o in log]
    orderform.item.choices = [(f.item, f.item) for f in models.Food.query.all()]
    context = {'name': name, 'orderform': orderform, 'myorders': myorderform, 'status': ' ',
               'price': ' ', 'date_out': ' '}
    if myorderform.is_submitted():
        order = models.Order.query.filter_by(
            id=models.OrderFoodLog.query.filter_by(id=myorderform.item.data).first().order_id).first()
        food = models.Food.query.filter_by(
            id=models.OrderFoodLog.query.filter_by(id=myorderform.item.data).first().food_id).first()
        if myorderform.option.data == 'Check Status':
            status='Status: '+order.status+'___'
            price='Price: '+str(food.price)+' EGP___'
            date_out='Date of Arrival: '+str(order.date_out)
            context['status'] = status
            context['price'] = price
            context['date_out'] = date_out
        elif myorderform.option.data == 'Cancel Order':
            models.db.session.delete(order)
            models.db.session.commit()
            return redirect(url_for('home', name=name))
    if orderform.validate_on_submit():
        order = models.Order(status='Order Received',date_in=datetime.datetime.now(), date_out=orderform.date.data, user=models.User.query.filter_by(username=name).first())
        ofl = models.OrderFoodLog(food =models.Food.query.filter_by(item=orderform.item.data).first(), order=order)
        flash(f'{orderform.item.data} has been ordered successfully!!')
        models.db.session.add(order)
        models.db.session.commit()
        return redirect(url_for('home', name=name))
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
