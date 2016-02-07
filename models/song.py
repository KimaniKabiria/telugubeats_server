
import bson
from mongoengine import Document, StringField, DateTimeField, IntField
import datetime
from mongoengine.fields import ListField, ReferenceField
from models.album import Album
from bson import json_util






class Song(Document):
    title = StringField()
    genre  = StringField()
    tags = ListField(StringField())
    lyricists = ListField(StringField())
    singers = ListField(StringField())
    rating = IntField()
    album = ReferenceField(Album)   
    track_n = IntField()# just a number
    path = StringField()#file path
    last_played = DateTimeField()
    
    
    def to_son(self):
        data = self.to_mongo()
        data["album"] = self.album.to_son()
        return data
    
    def to_json(self):
        return json_util.dumps(self.to_son())
    
class SongsMeta(Document):
    n = IntField()
    