from mongoengine.fields import IntField, ReferenceField, ListField, StringField,\
    DateTimeField
from models.song import Song, SongsMeta
from mongoengine.document import Document
import random
import datetime




class PollItem(Document):
    poll_count  = IntField()
    poll = ReferenceField('Poll')
    song = ReferenceField(Song)
    
    def to_son(self, use_db_field=True, fields=None):
        data = Document.to_mongo(self, use_db_field=use_db_field, fields=fields)
        data["song"] = self.song.to_son()
        return data
    
    
    def vote_up(self):
        self.poll_count+=1
        self.save()
    
    def vote_down(self):
        self.poll_count-=1
        self.poll_count = max(0 , self.poll_count)
        self.save()
        

class Poll(Document):
    poll_items = ListField(ReferenceField(PollItem))
    stream_id = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    
    
    
    def to_son(self, use_db_field=True, fields=None):
        data = Document.to_mongo(self, use_db_field=use_db_field, fields=fields)
        for i in range(len(data["poll_items"])):
            data["poll_items"][i] = self.poll_items[i].to_son()
        return data
    
    @classmethod
    def get_highest_poll_song(cls, stream_id):
        poll = cls.get_current_poll(stream_id)
        mx = -1
        mx_song = None
        for poll_item in poll.poll_items:
            poll_item.song = Song.objects(id=poll_item.song.id).get()
            print poll_item.song.title , poll_item.poll_count
            
            if(poll_item.poll_count>=mx):
                if(poll_item.poll_count==mx):
                    if(random.randint(0,1)==1):
                        continue
                mx = poll_item.poll_count
                mx_song = poll_item.song
        
        return mx_song
                
                
    @classmethod
    def get_current_poll(cls, stream_id):
        try:
            return Poll.objects(stream_id= stream_id).order_by('-created_at')[0]
        except Exception as ex:
            print ex
            return None
    
    @classmethod
    def create_next_poll(cls, stream_id):
        #pick , 7 songs, 
        # create poll items , 
        # create poll item with the stream Id
        #return 
        total_songs = SongsMeta.objects().get().n
        lst = set()
        while(len(lst)<7):
            lst.add(random.randint(0,total_songs))
        poll = Poll()
        poll.stream_id = stream_id
        poll.save()
        poll_items = []
        try:
            for i in lst:
                song = Song.objects(track_n=i).get()
                poll_item =  PollItem(song = song , poll_count =0 , poll= poll)
                poll_items.append(poll_item)
        
            for poll_item in poll_items:
                poll_item.save()
            
            poll.poll_items = poll_items
            poll.save()#again with updates pollItems
        except Exception as ex:
            print ex
            poll.delete()
            for poll_item in poll_items:
                poll_item.delete()
            
        return poll

        

        

class UserPolls(Document):
    user = ReferenceField('User')
    poll = ReferenceField('Poll')
    poll_item = ReferenceField('PollItem')
    
    #return old poll
   
        