

'''
handles events and audio listeners and initial data
'''

from bson import json_util
from enums import Event
from config import OK_200
from handlers.streams import streams, Stream
from models.song import Song
from datetime import datetime
from utils import user_auth, helper_funcs
from server.io_utils import response_write
from server.logger import logger
from server.config import OK_404
import traceback
import sys
from server.rt import connect_sink



@user_auth
def get_stream_info(socket, stream_id, query_params=None,user=None):
    socket.send(OK_200)
    stream = streams.get(stream_id)
    if(not stream):
        stream = Stream.objects(stream_id=stream_id).get()
    response_write(socket, json_util.dumps(stream.to_son()))
    socket.close()
    
@user_auth
def get_last_events(socket, stream_id, from_time_stamp , query_params=None,user=None):
    from_time_stamp = int(from_time_stamp)
    
    events = streams.get(stream_id).last_few_events.get(Event.CHAT_MESSAGE, [])
    socket.send(OK_200)
    response_write(socket, json_util.dumps([x.to_son()  for x in events]))
    socket.close()



def get_song_by_id(socket, song_id, query_params=None):
    response_write(socket, OK_200)
    response_write(socket, Song.objects(pk=song_id).to_json())
    socket.close()




@user_auth
def forward_audio_stream(socket, stream_id, user=None, query_params=None):
    stream = streams.get(stream_id)    
    if(not stream):
        stream = Stream.objects(stream_id=stream_id , user = str(user.id)).get()
        
    if(not stream or stream.is_live):
        response_write(socket,OK_404)
        logger.debug("stream already alive , cannot forward again")
        socket.close()
        return
    stream.initialize()
    response_write(socket,OK_200)
    logger.debug("reading audio now..")
    stream.forward_audio(socket)
    
    
    
@user_auth
def listen_audio_stream(socket, stream_id, query_params=None, user=None):
    streams.get(stream_id).stream_audio(socket)
    
#http and reader socket ?
@user_auth
def listen_events(socket, stream_id,query_params=None, user=None):
    response_write(socket, OK_200)
    streams.get(stream_id).add_event_listener(socket)
    connect_sink(socket,"telugubeats",stream_id)# don't break the connection



@user_auth
def get_live_audio_streams(socket,  page , query_params=None, user=None):
    page = int(page)
    streams = [x.to_son() for x in Stream.objects(is_live=True)[page*10:page*10+10]]
    response_write(socket, OK_200)
    response_write(socket,json_util.dumps(streams))
    socket.close()

@user_auth
def get_scheduled_streams(socket, page, query_params=None, user=None):
    page = int(page)
    streams = [x.to_son() for x in Stream.objects(is_scheduled__gt=datetime.now())[page*10:page*10+10]]
    response_write(socket, OK_200)
    response_write(socket,json_util.dumps(streams))
    socket.close()

@user_auth
def get_user_streams(socket, page, user=None, query_params=None):
    page = int(page)
    streams = [x.to_son() for x in Stream.objects(user= str(user.id))[page*10:page*10+10]]
    response_write(socket, OK_200)
    response_write(socket,json_util.dumps(streams))
    socket.close()

@user_auth
def create_stream(socket, user=None, query_params=None):
    new_steam = None
    while(True):
        try:
            new_stream = Stream()
            new_stream.stream_id = helper_funcs.get_random_id(10)
            new_stream.title = query_params["title"][0]
            new_stream.additional_info = query_params["additional_info"][0]
            new_stream.user = str(user.id)
            new_stream.is_special_song_stream = False
            new_stream.save() 
            break
        except:
            logger.debug(sys.exc_info())
            pass
    
    response_write(socket, OK_200)
    response_write(socket,json_util.dumps(new_stream.to_son()))
    socket.close()



    
@user_auth
def send_hearts(socket, stream_id, hearts_count ,query_params=None, user=None):
    hearts_count = int(hearts_count)
    streams.get(stream_id).publish_event(Event.HEARTS, str(hearts_count), user)
    response_write(socket, OK_200)
    response_write(socket, "ok")
    socket.close()    
