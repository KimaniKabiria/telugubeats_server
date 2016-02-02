import json
from gevent._threading import Semaphore
from gevent.greenlet import Greenlet
import gevent
import gevent.queue
from bson import json_util
from bson.son import SON
from config import OK_200
from models.events import StreamEvent
from enums import Event
from helpers.io_utils import response_write



class EventListeners:
    
    event_listeners = {} 
    event_queue = {}    
    
    last_few_events = {}
    last_reset_event  = {}
    def init_stream_listeners(self, stream_id):
        self.event_listeners[stream_id] = {}
        self.event_queue[stream_id] = gevent.queue.Queue()
        self.last_few_events[stream_id]  = StreamEvent.get_events(stream_id)
        
        Greenlet.spawn(EventListeners.start_publishing_events, self, stream_id)
        '''
        TODO : start reading from master server
        '''

            
            
        
    def publish_event(self, stream_id , event_id,  event_data , from_user=None):
        self.event_queue[stream_id].put({"event_id": event_id, "payload":event_data, "from_user": from_user})
        
                