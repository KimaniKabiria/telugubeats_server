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
    get_last_events, get_song_by_id
from mimetools import Message
from StringIO import StringIO
from helpers.auth import decode_signed_value
from models.user import User
import urlparse
from requests.polls import do_poll, get_current_poll, get_poll_by_id
from requests.users import do_register_user, do_dedicate_event, get_current_user
import urllib
from models import initDb
from requests import print_stats
from requests.chat import do_chat_event
from handlers.streams import Stream
from logger import logger

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
                    
                    ( re.compile("/get_stream_info/([^/]+)") , get_stream_info), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_current_poll/([^/]+)") , get_current_poll), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_last_events/([^/]+)/(.*)") , get_last_events), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_song_by_id/([^/]+)") , get_song_by_id), #"/poll/telugu/123123/12312312"
                    ( re.compile("/get_poll_by_id/([^/]+)") , get_poll_by_id), #"/poll/telugu/123123/12312312"
                    
                    ( re.compile("/poll/([^/]+)/([^/]+)/(.*)") , do_poll), #"/poll/telugu/123123/12312312"

                    
                    ( re.compile("/user/login") , do_register_user),
                    
                    ( re.compile("/get_current_user") , get_current_user),

                    ( re.compile("/dedicate/(.+)") , do_dedicate_event),
                    ( re.compile("/chat/(.+)") , do_chat_event),
                    ( re.compile("/stats") , print_stats),
                ]



def read_line(socket):
    data = ""
    while(True):
        byt = socket.recv(1)
        data+=byt
        if(byt=='\n' or not byt):
            return data
        
# this handler will be run for each incoming connection in a dedicated greenlet
def handle_connection(socket, address):
    
    
    request_line = read_line(socket)
    try:
        request_type , request_path , http_version = request_line.split(" ")
    except:
        socket.close()
    logger.debug("new request" +  request_line)
    headers = {}
    while(True):
        l = read_line(socket)
        if(l=='\r\n'):
            break
        if( not l):
            return
        header_type , data  =  l.split(": ",1)
        headers[header_type] = data
    post_data = None
    if(request_type == "POST" and headers.get("Content-Length", None)):
        n = int(headers.get("Content-Length","0").strip(" \r\n"))
        if(n>0):
            data = ""
            while(len(data) < n):
                bts = socket.recv(n)
                if(not bts):
                    break
                data +=bts
            post_data = urlparse.parse_qs(data)
    ##app specific headers
    auth_key = headers.get("auth-key", None)
    user = None
    if(auth_key):
        #decode and get user
        auth_key = urllib.unquote(auth_key).strip()
        user = User.objects.get(pk = decode_signed_value(config.SERVER_SECRET , "auth_key", auth_key))
        
    for handler in request_handlers:
        
        args = handler[0].match(request_path)
        func = handler[1]
        kwargs = {"user":user}
        if(post_data!=None):
            kwargs["post"] = post_data
        if(args!=None):
            fargs = args.groups()
            if(fargs):
                func(socket, *fargs , **kwargs)
            else:
                func(socket, **kwargs)

                
if __name__ == "__main__":
    
    initDb()
    #initialize reading and file decoder
    #keep reading streams , auto reconnecting 
    
    stream = Stream.objects(stream_id="telugu")
    if(stream):
        stream = stream[0]
    else:
        stream = Stream(stream_id="telugu", is_special_song_stream=True)
        stream.save()

    stream.initialize()
    
    logger.debug("stream initialized")
    server = StreamServer(
    ('', 8888), handle_connection)
    
    
    server.serve_forever()    

