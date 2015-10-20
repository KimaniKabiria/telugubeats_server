'''
Created on Oct 3, 2015

@author: abhinav
'''
from bson.son import SON
from bson import json_util


class PollChangeEvent:
    poll_id = None 
    count = 0
    song_title = None
    
    def __init__(self, poll_id , count , song_title):
        self.poll_id = poll_id
        self.count = count
        self.song_title = song_title
        
        
    def to_son(self):
        ret = SON()
        ret["poll_id"] = self.poll_id
        ret["count"] = self.count
        ret["song_title"]  = self.song_title
        return ret
    
    @classmethod
    def get_poll_changes_to_json(cls, poll_changes):
        ret = SON()
        ret["poll_changes"] = map(lambda x : x.to_son() , poll_changes) 
        return json_util.dumps(ret)
    
