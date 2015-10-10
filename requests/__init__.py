from gevent_handlers.events import EventListeners


## stream requesats init
stream_events_handler = EventListeners()



def init_stream_event_handlers():
    stream_events_handler.init_stream_listeners("telugu")