import mongoengine as me


class User(me.Document):
    username = me.StringField(required=True, unique=True)
    name = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    age = me.IntField()

    def __init__(self, username, name, email, password, age):
        self.username = username
        self.name = name
        self.email = email
        self.password_hash = password
        self.age = age

    def json(self):
        return {
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'age': self.age
        }
