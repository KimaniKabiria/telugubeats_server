from bson.son import SON
from gevent_handlers.events import EventListeners


class InitData():
    poll = None
    current_song = None
    user_poll_item_id = None;
    last_few_events = None
    user = None
    
    
    def to_son(self):
        ret = SON()
        ret["poll"] = self.poll.to_son()
        ret["current_song"] = self.current_song.to_son()
        if(self.user):   
            ret["user"] = self.user.to_son()
            ret["user_poll_item_id"]= self.user_poll_item_id
            
        ret["last_few_events"] = EventListeners.last_few_events
        
        return ret