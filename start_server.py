'''
Created on Sep 24, 2015

@author: abhinav
@lets_roll_babyo
'''

import time
from gevent import socket, greenlet
from gevent.server import StreamServer
import gevent.monkey
from gevent.greenlet import Greenlet
import os
import id3reader
import array
import config
import gevent
import re
from buffers import Buffer
from models.polls import PollItem, Poll
from models.song import Song
from mongoengine.connection import connect
from bson import json_util
from bson.son import SON
from requests.stream import listen_audio_stream, listen_events, get_stream_info,\
    get_last_events, get_song_by_id, send_hearts, get_live_audio_streams,\
    get_scheduled_streams, forward_audio_stream, get_user_streams, create_stream,\
    get_past_stream
from mimetools import Message
from StringIO import StringIO
from models.user import User
import urlparse
from requests.polls import do_poll, get_current_poll, get_poll_by_id
from requests.users import do_register_user, do_dedicate_event, get_current_user
import urllib
from requests import print_stats
from requests.chat import do_chat_event
from handlers.streams import Stream
from logger import logger
from _db import init_db
from server import start_httpsocket_server

gevent.monkey.patch_all()

#audio chunksize


    
#TODO:
# read from main streaming socket that just reads and file and dump raw bytes , 
# put that into streams , for now just do it with files(consider them as sockets)
# 
# write client handlers , handles clients , keep them in a list , 
# keep sending data from the streams continuously , break connection after sending few bytes 
# send metadata at times

#libevent , keep writing audio data to clients

#libevent , keep reading from the main stream

#libevent , keep broadcasting events , new polls , new chats etc


    

    
#this should internally spawn 

request_handlers = [(re.compile("/listen_audio_stream/([^/]+)")  ,  listen_audio_stream), #stream/telugu/audio or events
                    (re.compile("/listen_events/([^/]+)")  ,  listen_events), #stream/telugu/audio or events                    


                    ( re.compile("/send_hearts/([^/]+)/(.*)") , send_hearts), #"/poll/telugu/123123/12312312"                    
                    ( re.compile("/get_stream_info/([^/]+)") , get_stream_info), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_current_poll/([^/]+)") , get_current_poll), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_last_events/([^/]+)/(.*)") , get_last_events), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_song_by_id/([^/]+)") , get_song_by_id), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_poll_by_id/([^/]+)") , get_poll_by_id), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_past_stream/([^/]+)"), get_past_stream),
                    ( re.compile("/poll/([^/]+)/([^/]+)/(.*)") , do_poll), #"/poll/telugu/123123/12312312"

                    ( re.compile("/forward_stream/([^/]+)") ,forward_audio_stream), #"/poll/telugu/123123/12312312"

                    
                    ( re.compile("/get_live_audio_streams/([^/|^?]+)") , get_live_audio_streams), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_scheduled_audio_streams/([^/^?]+)") , get_scheduled_streams), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_user_streams/([^/^?]+)") , get_user_streams), #"/poll/telugu/123123/12312312"
                    ( re.compile("/create_stream") , create_stream), #"/poll/telugu/123123/12312312"

                    
                    ( re.compile("/user/login") , do_register_user),
                    
                    ( re.compile("/get_current_user") , get_current_user),

                    ( re.compile("/dedicate/(.+)") , do_dedicate_event),
                    ( re.compile("/chat/(.+)") , do_chat_event),
                    ( re.compile("/stats") , print_stats),
                ]



if __name__ == "__main__":
    
    init_db(**config.db_server)
    #initialize reading and file decoder
    #keep reading streams , auto reconnecting 
    
    stream = Stream.objects(stream_id="telugu")
    if(stream):
        stream = stream[0]
    else:
        stream = Stream(stream_id="telugu", is_special_song_stream=True, is_live=True)
        stream.save()

    stream.initialize()
    
    logger.debug("stream initialized")
    
    start_httpsocket_server(request_handlers)
