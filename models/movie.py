import mongoengine as me


class Movie(me.Document):
    name = me.StringField(required=True, unique=True)
    genre = me.ListField(me.StringField(required=True))

    def json(self):
        return {'name': self.name, 'genre': self.genre}
