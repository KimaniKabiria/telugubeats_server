from mongoengine.document import Document
from mongoengine.fields import StringField, ListField, DateTimeField
from mongoengine.signals import pre_save
import datetime



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
        return [ i.data for i in StreamEvent.objects().order_by("-updated_at")[:20]]