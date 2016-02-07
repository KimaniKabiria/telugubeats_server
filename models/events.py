from mongoengine.document import Document
from mongoengine.fields import StringField, ListField, DateTimeField,\
    ReferenceField
from mongoengine.signals import pre_save
import datetime
from enums import Event
from bson import json_util
from logger import logger
from models.user import User



class StreamEvent(Document):
    stream_id = StringField()
    event_id = StringField()
    data = StringField()
    from_user = ReferenceField(User) # user id here
    tags = ListField(StringField())
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
    
    
    
    
    @classmethod
    def add(cls , stream_id , event_id ,  data , tags=[]):
        logger.debug("adding "+event_id+" to "+stream_id)
        event = StreamEvent(stream_id = stream_id , event_id=event_id,  data = data , tags = tags)
        event.save()
        return event
    
    @classmethod
    def get_events(cls, stream_id, n = 20):
        events = StreamEvent.objects(stream_id = stream_id).order_by("-updated_at")[:20]
        return map(lambda x : x, events)
    
    
    def to_son(self):
        son = self.to_mongo()
        if(self.from_user):
            son["from_user"] = self.from_user.to_short_son()
        return son
    
    
    def to_json(self):
        return json_util.dumps(self.to_son())