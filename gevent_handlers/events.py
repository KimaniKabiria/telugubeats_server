import json
from gevent._threading import Semaphore
from gevent.greenlet import Greenlet
import gevent
import gevent.queue
from bson import json_util
from bson.son import SON
from config import OK_200



class EventListeners:
    
    event_listeners = {} 
    event_queue = {}    
    
    last_few_events = []
    
    def init_stream_listeners(self, stream_id):
        self.event_listeners[stream_id] = {}
        self.event_queue[stream_id] = gevent.queue.Queue()
        
        Greenlet.spawn(EventListeners.start_publishing_events, self, stream_id)
        '''
        TODO : start reading from master server
        '''
    def add_listener(self, stream_id , socket):
        if(self.event_listeners.get(stream_id, None)==None):
            self.init_stream_listeners(stream_id)
            
        socket.send(OK_200)
        self.event_listeners[stream_id][socket] = True
    
    
    def send_event(self, stream_id , socket, data_to_send):
        try:
            socket.send(data_to_send)
            socket.send("\r\n\r\n")# stop word 
        except:
            del self.event_listeners[stream_id][socket] # remove the socket
    
    
    def start_publishing_events(self, stream_id):
        while(True):
            event_data = self.event_queue[stream_id].get()
            data_to_send = json_util.dumps(event_data).replace("\r\n", "\n\n")
            
            EventListeners.last_few_events.append(data_to_send)
            if(len(EventListeners.last_few_events)>20):
                EventListeners.pop(0)
                
            for socket in self.event_listeners[stream_id]:
                # send data in parallel ?
                Greenlet.spawn(EventListeners.send_event , self, stream_id , socket, data_to_send)
            
            
        
    def publish_event(self, stream_id , event_id,  event_data , from_user=None):
        #bulk publishing, is this correct ? TODO:
        self.event_queue[stream_id].put({"event_id": event_id, "payload":event_data, "from_user": from_user})
        
                