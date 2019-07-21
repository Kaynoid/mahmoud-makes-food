from app import db

class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    def __reper__(self):
        return f'<User {self.username}'


class Dish(db.Model):
    __table__name = 'dish'
    id = db.Column(db.Integer, primary_key=True)
    dish = db.Column(db.String(15))


class Side(db.Model):
    __table__name = 'side'
    id = db.Column(db.Integer, primary_key=True)
    side = db.Column(db.String(15))


class Drink(db.Model):
    __table__name = 'drink'
    id = db.Column(db.Integer, primary_key=True)
    drink = db.Column(db.String(15))

