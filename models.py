from app import db

class User(db.Model):
    __table__name = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    def __reper__(self):
        return f'<User {self.username}'


class Food(db.Model):
    __table__name = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(15))
    side = db.Column(db.String(15))
    drink = db.Column(db.String(15))

