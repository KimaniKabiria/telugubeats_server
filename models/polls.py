from mongoengine.fields import IntField, ReferenceField, ListField, StringField,\
    DateTimeField
from models.song import Song, SongsMeta
from mongoengine.document import Document
import random
import datetime
from mongoengine.errors import MultipleObjectsReturned, DoesNotExist
from bson.son import SON




class PollItem(Document):
    poll_count  = IntField()
    poll = ReferenceField('Poll')
    song = ReferenceField(Song)
    
    def to_son(self, use_db_field=True, fields=None):
        data = SON()
        data["_id"] = self.id
        data["poll_count"] = self.poll_count
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
        data = SON()
        data["_id"] = self.id
        data["stream_id"] = self.stream_id
        data["created_at"] = self.created_at
        data["poll_items"] = [None for x in range(len(self.poll_items))]
        for i in range(len(self.poll_items)):
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
    def create_next_poll(cls, stream_id , save_in_db = True):
        #pick , 7 songs, 
        # create poll items , 
        # create poll item with the stream Id
        #return 
        total_songs = SongsMeta.objects().get().n
            
        poll = Poll()
        poll.stream_id = stream_id
        if(save_in_db):
            poll.save()
        poll_items = []
        try:
            temp_track_hash = {}
            while(len(poll_items)<7):
                try:
                    random_track_n = random.randint(0,total_songs)
                    if(temp_track_hash.get(random_track_n, None)): continue# dont repeat tracks
                    
                    song = Song.objects(track_n=random_track_n).get()
                    poll_item =  PollItem(song = song , poll_count =0 , poll= poll)
                    poll_items.append(poll_item)
                    temp_track_hash[random_track_n] = True
                    
                except (MultipleObjectsReturned, DoesNotExist) as ex:
                    pass
                
                    
            for poll_item in poll_items:
                if(save_in_db): 
                    poll_item.save()
            
            poll.poll_items = poll_items
            if(save_in_db):
                poll.save()#again with updates pollItems
        except Exception as ex:
            print ex
            poll.delete()
            poll = None
            for poll_item in poll_items:
                if(save_in_db):
                    poll_item.delete()
            
        return poll

        

        

class UserPolls(Document):
    user = ReferenceField('User')
    poll = ReferenceField('Poll')
    poll_item = ReferenceField('PollItem')
    
    #return old poll
   
        