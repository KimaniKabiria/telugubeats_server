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
from events import EventListeners
from gevent_handlers.audio_streams import AudioStreamReader, handle_audio_stream
from models.polls import PollItem, Poll
from models.song import Song
from mongoengine.connection import connect
from bson import json_util
from bson.son import SON
from gevent_handlers import init_main_audio_streams
from requests.stream import do_stream_request 
from mimetools import Message
from StringIO import StringIO
from helpers.auth import decode_signed_value
from models.user import User
import urlparse
from requests.polls import do_poll
from requests.users import do_register_user
import urllib

gevent.monkey.patch_socket()



def initDb():
    dbServer = {"dbName":"quizApp",
                       "ip":"0.0.0.0",# "db.quizapp.appsandlabs.com",
                       "port": 27017,
                       "username": "quizapp",
                       "password":"XXXXX"
       }
    dbConnection = connect(dbServer["dbName"], host=dbServer["ip"], port=dbServer["port"])
    
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

request_handlers = [(re.compile("stream/([^/]+)/(.*)")  ,  do_stream_request), #stream/telugu/audio or events
                    ( re.compile("poll/([^/]+)/([^/]+)/(.*)") , do_poll), #"/poll/telugu/123123/12312312"
                    ( re.compile("user/login") , do_register_user), #"/poll/telugu/123123/12312312"
                   ]


# this handler will be run for each incoming connection in a dedicated greenlet
def handle_connection(socket, address):
    print('New connection from %s:%s' % address)
        
    socket_file = socket.makefile('r')    
    request_line = socket_file.readline()
    request_type , request_path , http_version = request_line.split(" ")
    headers = {}
    while(True):
        l = socket_file.readline()
        if(l=='\r\n'):
            break
        
        header_type , data  =  l.split(": ",1)
        headers[header_type] = data

    post_data = None
    if(request_type == "POST" and headers.get("Content-Length", None)):
        n = int(headers.get("Content-Length",0))
        data = ""
        while(len(data) < n):
            data += socket.recv(n)
        post_data = urlparse.parse_qs(data)
        
    ##app specific headers
    auth_key = headers.get("auth_key", None)
    user = None
    if(auth_key):
        #decode and get user
        auth_key = urllib.unquote(auth_key).strip()
        user = User.objects.get(pk = decode_signed_value(config.SERVER_SECRET , "auth_key", auth_key))
        
    for handler in request_handlers:
        args = handler[0].findall(request_path)
        func = handler[1]
        kwargs = {"user":user}
        if(post_data):
            kwargs["post"] = post_data
        if(args):
            if(isinstance(args[0],tuple)):
                func(socket, *args[0] , **kwargs)
            else:
                func(socket, **kwargs)
                
if __name__ == "__main__":
    
    initDb()
    #initialize reading and file decoder
    #keep reading streams , auto reconnecting 
    init_main_audio_streams()
    
    
    server = StreamServer(
    ('', 8888), handle_connection)
    
    
    server.serve_forever()    

