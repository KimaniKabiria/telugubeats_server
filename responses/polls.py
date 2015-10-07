'''
Created on Oct 3, 2015

@author: abhinav
'''
from bson.son import SON
from bson import json_util


class PollChangeEvent:
    poll_id = None 
    count = 0
    def __init__(self, poll_id , count ):
        self.poll_id = poll_id
        self.count = count
        
        
    def to_son(self):
        ret = SON()
        ret["poll_id"] = self.poll_id
        ret["count"] = self.count
        return ret
    
    @classmethod
    def get_poll_changes_to_json(cls, poll_changes):
        ret = SON()
        ret["poll_changes"] = map(lambda x : x.to_son() , poll_changes) 
        return json_util.dumps(ret)
    
