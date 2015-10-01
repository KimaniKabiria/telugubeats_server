
import bson
from mongoengine import Document, StringField, DateTimeField, IntField
import datetime
from mongoengine.fields import ListField, ReferenceField
from models.album import Album

class Song(Document):
    title = StringField()
    genre  = StringField()
    tags = ListField(StringField())
    lyricists = ListField(StringField())
    singers = ListField(StringField())
    rating = IntField()
    album = ReferenceField(Album)
    
    