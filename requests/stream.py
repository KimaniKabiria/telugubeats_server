

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
from handlers.streams import streams, Stream




def get_stream_info(socket, stream_id, user=None):
    socket.send(OK_200)
    response_write(socket, json_util.dumps(streams.get(stream_id).to_mongo()))


def get_last_events(socket, stream_id, user=None):
    
    events = streams.get(stream_id).last_few_events    
    socket.send(OK_200)
    response_write(socket, json_util.dumps(events))
    socket.close()



def listen_audio_stream(socket, stream_id, user=None):
    audio_streams.handle_audio_stream(stream_id, socket)
    
#http and reader socket ?
def listen_events(socket, stream_id, user=None):
    response_write(socket, OK_200)
    streams.get(stream_id).add_event_listener(socket)
    
