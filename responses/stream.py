from bson.son import SON
from gevent_handlers.events import EventListeners
from requests import stream_events_handler


class InitData():
    poll = None
    current_song = None
    user_poll_item_id = None;
    last_few_events = None
    user = None
    n_user = None
    
    def to_son(self):
        ret = SON()
        ret["poll"] = self.poll.to_son()
        ret["current_song"] = self.current_song.to_son()
        if(self.user):   
            ret["user"] = self.user.to_son()
            ret["user_poll_item_id"]= self.user_poll_item_id
            
        ret["last_few_events"] = self.last_few_events
        ret["n_users"] = self.n_user
        return ret