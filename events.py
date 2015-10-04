import json
from gevent._threading import Semaphore
from gevent.greenlet import Greenlet
import gevent
from bson import json_util
from bson.son import SON



class EventListeners:
    
    event_listeners = {} 
    event_queue = {}    
    
    
    
    def init_stream_listeners(self, stream_id):
        self.event_listeners[stream_id] = {}
        self.event_queue[stream_id] = queue = gevent.queue.Queue()
        
        Greenlet.spawn(EventListeners.start_publishing_events, self, stream_id, queue)
        '''
        TODO : start reading from master server
        '''
    def add_listener(self, stream_id , socket):
        if(self.event_listeners.get(stream_id, None)==None):
            self.init_stream_listeners(stream_id)
            
        self.event_listeners[stream_id][socket] = True
    
    
    def send_event(self, socket, data_to_send):
        try:
            socket.send(data_to_send)
            socket.send("\r\n")# stop word 
        except:
            del self.event_listeners[socket] # remove the socket
    
    
    def start_publishing_events(self, stream_id, queue):
        while(True):
            event_data = queue.get()
            data_to_send = json_util.dumps(event_data).replace("\r\n", "\n\n")
            print data_to_send
            for socket in self.event_listeners[stream_id]:
                # send data in parallel ?
                Greenlet.spawn(EventListeners.send_event , self, socket, data_to_send)
            
            
        
    def publish_event(self, stream_id , event_id,  event_data , from_user=None):
        #bulk publishing, is this correct ? TODO:
        self.event_queue[stream_id].put({"event_id": event_id, "payload":event_data, "from_user": from_user})
        
                