from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
db = SQLAlchemy()

class User(UserMixin, db.Model):
    __table_name__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    is_admin = db.Column(db.Boolean, default=False)


class Food(db.Model):
    __table_name__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(32))
    price = db.Column(db.Integer)


class Order(db.Model):
    __table_name__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32)) #[Order Received, In Progress, Delivered]
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
