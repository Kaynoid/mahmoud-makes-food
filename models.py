from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)


class Food(db.Model):
    __table_name__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(15), unique=True)
    category = db.Column(db.String(10))
    price = db.Column(db.Integer)


class Order(db.Model):
    __table_name__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32)) #[order received, in progress, delivered]
    date_in = db.Column(db.DateTime)
    date_out = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('orders', lazy=True))


class OrderFoodLog(db.Model):
    __table_name__ = 'order_food_logs'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    food = db.relationship('Food', backref=db.backref('order_food_logs', lazy=True))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order', backref=db.backref('order_food_logs', lazy=True))
