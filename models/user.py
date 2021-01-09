import mongoengine as me


class User(me.Document):
    email = me.StringField(required=True, unique=True)
    username = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    name = me.StringField(required=True)

    # def __init__(self, email=None, password=None, name=None):
    #     self.email = email
    #     self.password_hash = password
    #     self.name = name

    def json(self):
        return {
            'name': self.name,
            'username': self.username,
            'email': self.email
        }
