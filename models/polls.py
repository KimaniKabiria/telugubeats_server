from mongoengine.fields import IntField, ReferenceField, ListField
from models.song import Song
from mongoengine.document import Document




class PollItem(Document):
    poll_ount  = IntField()
    song = ReferenceField(Song);

class Poll(Document):
    poll_items = ListField(PollItem)
    