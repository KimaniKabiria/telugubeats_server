

'''
handles events and audio listeners and initial data
'''

from bson import json_util
from enums import Event
from helpers.io_utils import response_write
from config import OK_200
from handlers.streams import streams, Stream
from models.song import Song




def get_stream_info(socket, stream_id, user=None):
    socket.send(OK_200)
    response_write(socket, json_util.dumps(streams.get(stream_id).to_mongo()))
    socket.close()

def get_last_events(socket, stream_id, from_time_stamp , user=None):
    from_time_stamp = int(from_time_stamp)
    
    events = streams.get(stream_id).last_few_events    
    socket.send(OK_200)
    response_write(socket, json_util.dumps([x.to_son()  for x in events]))
    socket.close()



def get_song_by_id(socket, song_id):
    response_write(socket, OK_200)
    response_write(socket, Song.objects(pk=song_id).to_json())
    socket.close()



def listen_audio_stream(socket, stream_id, user=None):
    streams.get(stream_id).stream_audio(socket)
    
#http and reader socket ?
def listen_events(socket, stream_id, user=None):
    response_write(socket, OK_200)
    streams.get(stream_id).add_event_listener(socket)
    
