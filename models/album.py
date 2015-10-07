from mongoengine.document import Document
from mongoengine.fields import StringField, ListField



class Album(Document):
    name = StringField()
    directors = ListField(StringField());
    music_directors = ListField(StringField())
    actors = ListField(StringField());
    image_url = StringField()
    
    def to_son(self):
        return self.to_mongo()