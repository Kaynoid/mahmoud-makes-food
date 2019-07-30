from datetime import datetime
import os
import datetime
from flask import Flask, jsonify, render_template, url_for, redirect, flash
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import forms
from flask_login import login_user, logout_user, LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
login_manager = LoginManager(app)
login_manager.login_view = 'app.login'
import models
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
        user = models.User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('This user does not exist!','error')
            return redirect(url_for('login'))
        elif user.verify_password(form.password.data):
            if user.is_admin:
                login_user(user, form.remember.data)
                return redirect(url_for('admin_home', name=user.username))
            else:
                login_user(user, form.remember.data)
                return redirect(url_for('home', name=user.username))
    return render_template('login.html', **context)


@app.route('/home/<name>', methods=['GET', 'POST'])
def home(name):
    orderform = forms.OrderForm()
    myorderform = forms.MyOrdersForm()
    user_id =  models.User.query.filter_by(username=name).first().id
    user_orders = models.Order.query.filter_by(user_id=user_id)
    order_ids = [o.id for o in user_orders]
    for o in order_ids:
        ofl = models.OrderFoodLog.query.filter_by(order_id=o)
        if ofl.count()==3:
            myorderform.item.choices.insert(len(myorderform.item.choices),(o,ofl[0].food.item + ' with ' + ofl[1].food.item + ' and ' + ofl[2].food.item))
        elif ofl.count()==2:
            myorderform.item.choices.insert(len(myorderform.item.choices),(o, ofl[0].food.item + ' with ' + ofl[1].food.item))
        elif ofl.count()==1:
            myorderform.item.choices.insert(len(myorderform.item.choices),(o, ofl[0].food.item))
    orderform.main.choices = [(f.item, f.item + ' - ' + str(f.price)+' EGP') for f in models.Food.query.filter_by(category='Main Dish')]
    orderform.side.choices = [(f.item, f.item + ' - ' + str(f.price)+' EGP') for f in models.Food.query.filter_by(category='Side Dish')]
    orderform.drink.choices = [(f.item, f.item + ' - ' + str(f.price)+' EGP') for f in models.Food.query.filter_by(category='Drink')]
    orderform.main.choices.insert(0, ('Nothing','-'))
    orderform.side.choices.insert(0, ('Nothing', '-'))
    orderform.drink.choices.insert(0, ('Nothing', '-'))
    context = {'name': name, 'orderform': orderform, 'myorders': myorderform, 'status': ' ',
               'price': ' ', 'date_out': ' '}
    if myorderform.is_submitted():
        if myorderform.item.data == '-':
            flash(f'You must choose an order to proceed!')
            return redirect(url_for('home', name=name))
        else:
            if models.OrderFoodLog.query.filter_by(order_id=myorderform.item.data).first():
                order_id = myorderform.item.data
                order = models.Order.query.filter_by(id=order_id).first()
            if myorderform.option.data == 'Check Status':
                status = 'Status: ' + order.status + ' - '
                foodlog = models.OrderFoodLog.query.filter_by(order_id=order_id)
                if foodlog.count() == 3:
                    total_price = foodlog[0].food.price + foodlog[1].food.price + foodlog[2].food.price
                elif foodlog.count() == 2:
                    total_price = foodlog[0].food.price + foodlog[1].food.price
                elif foodlog.count() == 1:
                    total_price = foodlog[0].food.price
                price = 'Total Price: ' + str(total_price) + ' EGP - '
                date_out = 'Date of Arrival: ' + str(order.date_out)
                context['status'] = status
                context['price'] = price
                context['date_out'] = date_out
            elif myorderform.option.data == 'Cancel Order':
                foodlog = models.OrderFoodLog.query.filter_by(order_id=order_id)
                if foodlog.count() == 3:
                    models.db.session.delete(foodlog[0])
                    models.db.session.delete(foodlog[0])
                    models.db.session.delete(foodlog[0])
                elif foodlog.count() == 2:
                    models.db.session.delete(foodlog[0])
                    models.db.session.delete(foodlog[0])
                elif foodlog.count() == 1:
                    models.db.session.delete(foodlog[0])
                models.db.session.delete(order)
                models.db.session.commit()
                flash(f'Your order has been cancelled.')
                return redirect(url_for('home', name=name, context=context))
    return render_template('home.html', **context)


@app.route('/home/<name>/order', methods=['POST'])
def order(name):
    orderform = forms.OrderForm()
    if orderform.main.data != 'Nothing' or orderform.side.data != 'Nothing' or orderform.drink.data != 'Nothing':
        order = models.Order(status='Order Received', date_in=datetime.datetime.now(), date_out=orderform.date.data,
                             user=models.User.query.filter_by(username=name).first())
        if orderform.main.data != 'Nothing':
            ofl = models.OrderFoodLog(food=models.Food.query.filter_by(item=orderform.main.data).first(), order=order)
            flash(f'{orderform.main.data} has been ordered successfully!!')
        if orderform.side.data != 'Nothing':
            ofl = models.OrderFoodLog(food=models.Food.query.filter_by(item=orderform.side.data).first(), order=order)
            flash(f'{orderform.side.data} has been ordered successfully!!')
        if orderform.drink.data != 'Nothing':
            ofl = models.OrderFoodLog(food=models.Food.query.filter_by(item=orderform.drink.data).first(), order=order)
            flash(f'{orderform.drink.data} has been ordered successfully!!')
        models.db.session.add(order)
        models.db.session.commit()
        return redirect(url_for('home', name=name))
    else:
        flash(f'Sorry! You must choose atleast one item to make an order.')
        return redirect(url_for('home', name=name))


@app.route('/admin/<name>', methods=['GET', 'POST'])
def admin_home(name):
    addform = forms.AdminAddForm()
    removeform = forms.AdminRemoveForm()
    removeform.item.choices = [(f.item, f.item) for f in models.Food.query.all()]
    removeform.item.choices.insert(0,('-','-'))
    manageorderform = forms.ManageOrdersForm()
    order_ids = [o.id for o in models.Order.query.all()]
    for o in order_ids:
        ofl = models.OrderFoodLog.query.filter_by(order_id=o)
        if ofl.count()==3:
            manageorderform.order.choices.insert(len(manageorderform.order.choices),(o,ofl[0].food.item + ' with ' + ofl[1].food.item + ' and ' + ofl[2].food.item + ' for ' + ofl[0].order.user.username +' - '+ ofl[0].order.status))
        elif ofl.count()==2:
            manageorderform.order.choices.insert(len(manageorderform.order.choices),(o, ofl[0].food.item + ' with ' + ofl[1].food.item + ' for ' + ofl[0].order.user.username +' - '+ ofl[0].order.status))
        elif ofl.count()==1:
            manageorderform.order.choices.insert(len(manageorderform.order.choices),(o, ofl[0].food.item + ' for ' + ofl[0].order.user.username +' - '+ ofl[0].order.status))
    context = {'name' : name, 'addform' : addform, 'removeform' : removeform, 'manageorderform': manageorderform}
    return render_template('admin_home.html', **context)

@app.route('/admin/<name>/add', methods=['POST'])
def admin_add(name):
    addform = forms.AdminAddForm()
    item = models.Food(item=addform.item.data, category=addform.category.data, price=addform.price.data)
    models.db.session.add(item)
    models.db.session.commit()
    flash(f'{item.item.capitalize()} was added succesfully', 'info')
    return redirect(url_for('admin_home', name=name))


@app.route('/admin/<name>/manage_order', methods=['POST'])
def admin_manage(name):
    manageorderform = forms.ManageOrdersForm()
    if manageorderform.order.data == '-':
        flash(f'You must choose an order to proceed!')
        return redirect(url_for('admin_home', name=name))
    else:
        if models.OrderFoodLog.query.filter_by(order_id=manageorderform.order.data).first():
            order_id = manageorderform.order.data
            order = models.Order.query.filter_by(id=order_id).first()
        if manageorderform.option.data == 'Remove Order':
            foodlog = models.OrderFoodLog.query.filter_by(order_id=order_id)
            if foodlog.count() == 3:
                models.db.session.delete(foodlog[0])
                models.db.session.delete(foodlog[0])
                models.db.session.delete(foodlog[0])
            elif foodlog.count() == 2:
                models.db.session.delete(foodlog[0])
                models.db.session.delete(foodlog[0])
            elif foodlog.count() == 1:
                models.db.session.delete(foodlog[0])
            models.db.session.delete(order)
            models.db.session.commit()
            flash(f'Order has been removed successfully!')
        elif manageorderform.option.data == "Set Status":
            order.status = manageorderform.status.data
            models.db.session.commit()
            flash(f'Order status has been changed to {manageorderform.status.data}')
        return redirect(url_for('admin_home', name=name))


@app.route('/admin/<name>/remove', methods=['POST'])
def admin_remove(name):
    removeform = forms.AdminRemoveForm()
    if removeform.item.data != '-':
        item = models.Food.query.filter_by(item=removeform.item.data).first()
        models.db.session.delete(item)
        models.db.session.commit()
        flash(f'{item.item.capitalize()} has been removed successfully!')
    return redirect(url_for('admin_home', name=name))
