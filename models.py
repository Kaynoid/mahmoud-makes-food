from peewee import*

DB = "foodeaters.db"
db = SqliteDatabase(DB)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique = True)
    password = CharField()
    is_admin = BooleanField(default=False)


class Meal(BaseModel):
    meal_type = CharField()
    date = DateTimeField()


def run_db():
    db.connect()
    db.create_tables([User,Meal],safe=True)

