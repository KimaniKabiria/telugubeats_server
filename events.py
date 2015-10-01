import json
from gevent._threading import Semaphore



class EventListeners:
    
    event_listeners = {"telugu":{}} 
    event_lock = {}    
    
    
    def start_reading_events(self):
        '''start reading from msater server'''
        pass
    
    
    def create_stream(self, stream_id):
        self.event_listeners[stream_id] = {}
        self.event_lock[stream_id] = Semaphore()

    def add_listener(self, stream_id , socket):
        if(self.event_listeners.get(stream_id, None)==None):
            self.create_stream(stream_id)
        self.event_listeners[stream_id][socket] = True
    
    def publish_event(self, event,  stream_id , event_id , payload=True):
        #bulk publishing, is this correct ? TODO:
        self.event_lock[stream_id].acquire()
        
        data_to_send  = json.dumps({event_id:payload})
        for socket in self.event_listeners[stream_id]:
            try:
                socket.send(data_to_send)
                socket.send("\r\n")
            except:
                del self.event_listeners[socket] # remove the socket
                
        self.event_lock[stream_id].release()
