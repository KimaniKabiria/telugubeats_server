from mongoengine.document import Document
from mongoengine.fields import StringField, ListField, DateTimeField
from mongoengine.signals import pre_save
import datetime
from enums import Event
from bson import json_util



class StreamEvent(Document):
    stream_id = StringField()
    data = StringField()
    tags = ListField(StringField())
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    
    @classmethod
    def add(cls , stream_id , data , tags=[]):
        event = StreamEvent(stream_id = stream_id , data = data , tags = tags)
        event.save()
        return event
    
    @classmethod
    def get_events(cls, stream_id, n = 20):
        events = map(lambda x : json_util.loads(x) , [ i.data for i in StreamEvent.objects().order_by("-updated_at")[:20]])
        events = filter(lambda x : x["event_id"]!=Event.RESET_POLLS_AND_SONG , events)
        return map(lambda x :json_util.dumps(x) , events)
    
    