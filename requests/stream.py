

'''
handles events and audio listeners and initial data
'''
from requests import stream_events_handler

from requests.users import send_init_data
from gevent_handlers import audio_streams
from models import get_init_data
from bson import json_util
from enums import Event
from helpers.io_utils import response_write
from config import OK_200





def audio_stream(socket, stream_id):
    audio_streams.handle_audio_stream(stream_id, socket)
    

def events_stream(socket, stream_id, should_renew=None):
    pass    
    
    

def do_stream_request(socket, stream_id, stream_request_type, user = None):
    
        if(stream_request_type=="events"):
            stream_events_handler.add_listener(stream_id, socket)
            #send latest reset here
            
        if(stream_request_type=="events_renew"):            
            init_data = get_init_data(stream_id, user)            
            reset_event = {"event_id": Event.RESET_POLLS_AND_SONG, "payload":json_util.dumps(init_data.to_son()), "from_user": user}
            response_write(socket, OK_200)
                  
            stream_events_handler.send_event(stream_id, socket, json_util.dumps(reset_event).replace("\r\n", "\n\n"))
            stream_events_handler.add_listener(stream_id, socket , False)
            
        elif(stream_request_type=="audio"):
            # periodically send data , most important
            audio_streams.handle_audio_stream(stream_id, socket)
            
        elif(stream_request_type=="init_data"):
            send_init_data(socket , stream_id, user)