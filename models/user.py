'''
Created on Oct 3, 2015

@author: abhinav
'''
from mongoengine.fields import StringField, EmailField, FloatField, BooleanField,\
    IntField, DateTimeField, ListField, ReferenceField
from mongoengine.document import Document
from models.polls import UserPolls, PollItem
from mongoengine.errors import DoesNotExist
from bson.son import SON
from bson.dbref import DBRef
from bson.objectid import ObjectId

class User(Document):
    name = StringField()
    device_id = StringField(required=True)
    email_id = EmailField()
    picture_url = StringField()  # cdn link
    cover_url = StringField()
    birthday = FloatField()
    gender = StringField()
    place = StringField()
    country = StringField(default=None)
    ip_address = StringField()
    is_activated = BooleanField(default=False)
    gcm_reg_id = StringField()
    status = StringField()
    
    loginIndex = IntField()
    google_plus_token = StringField(default=None)
    facebook_token = StringField(default=None) 
    google_plus_uid = StringField() 
    fb_uid = StringField()
    createdAt = DateTimeField()
    gPlusFriends = StringField()
    fbFriends = StringField()
    
    
    def to_son(self):
        return self.to_mongo()
    
    
    def to_short_mongo(self):
        ret = SON()
        ret["name"] = self.name
        ret["_id"] = self.id
        return ret
    
    @classmethod
    def register_user(cls, **kwargs):
        email_id = kwargs.get('email_id',None)
        fb_uid = kwargs.get('fb_uid',None)
        google_plus_uid = kwargs.get('google_plus_uid',None)
        
        if(email_id):
            user = User.objects(email_id = email_id).all()
            if(user):
                user = user[0]
        if(not user and google_plus_uid):
            user = User.objects(google_plus_uid=google_plus_uid).all()
            if(user):
                user = user[0]
        if(not user and fb_uid):
            user = User.objects(fb_uid=fb_uid).all()
            if(user):
                user = user[0]
        if(not user):
            user = User()
        for key in kwargs:
            setattr(user, key , kwargs[key])
        user.save()
        return user
        
    def register_gcm(self, gcm_id):
        self.gcm_reg_id = gcm_id
        self.save()
        
        
    def get_poll_item(self, poll):
        try:
            user_poll = UserPolls.objects(user= self , poll = poll).get()
            return user_poll.poll_item
        except Exception as ex:
            print ex
            return None
    #returns old poll data to 
    def do_poll(self , poll_id , poll_item_id):
        
        new_poll_item = PollItem.objects(pk = poll_item_id).get()
        try:
            user_poll = UserPolls.objects(user= self , poll = ObjectId(poll_id)).get()
            
            old_poll = user_poll.poll_item
            # change to new poll
            user_poll.poll_item = ObjectId(poll_item_id)
            user_poll.save(validate=False)
            
            if(old_poll.id!=poll_item_id):
                new_poll_item.vote_up()
                old_poll.vote_down()    
            
            return str(old_poll.id), old_poll.song.title , poll_item_id, new_poll_item.song.title
            
        except DoesNotExist:
            user_poll = UserPolls(user= self , 
                                  poll = ObjectId(poll_id),
                                  poll_item = ObjectId(poll_item_id))
            user_poll.save()
            return None, None, poll_item_id, new_poll_item.song.title
        
    
    