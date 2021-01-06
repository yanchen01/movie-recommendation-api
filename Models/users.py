import mongoengine as me


class User(me.Document):
    username = me.StringField(required=True, unique=True)
    name = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    age = me.IntField()