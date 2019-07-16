from peewee import*

DB = "shoppinglist.db"
db = SqliteDatabase(DB)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique = True)
    password = CharField()

