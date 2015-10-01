from mongoengine.document import Document
from mongoengine.fields import StringField, ListField



class Album(Document):
    name = StringField()
    directors = ListField(StringField());
    music_directors = ListField(StringField())
    actors = ListField(StringField());
    imageUrl = StringField()