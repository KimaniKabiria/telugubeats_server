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
import dbutils
import polls
from events import EventListeners
from audio_streams import AudioStreamReader, handle_audio_stream
from models.polls import PollItem, Poll
from models.song import Song
from mongoengine.connection import connect
from bson import json_util
from bson.son import SON
gevent.monkey.patch_socket()

stream_path = re.compile("/([^/]+)/(.+)")


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


def send_init_data(socket , address , stream_id):
    song = Song.objects().get()
    poll = Poll()
    poll_item = PollItem(poll_count =10 , song = song)    
    poll.poll_items= [poll_item , poll_item , poll_item , poll_item]
    
    
    poll_data = SON()
    poll_data["poll"] = poll.to_mongo()
    poll_data["song" ] = song.to_mongo()
    poll_data = json_util.dumps(poll_data)
    socket.send(poll_data)
    socket.close()
    
    

    
#this should internally spawn 
events_handler = EventListeners()




# this handler will be run for each incoming connection in a dedicated greenlet
def handle_connection(socket, address):
    print('New connection from %s:%s' % address)
    
    headers = socket.recv(1024)
    request_type , request_path , http_version = headers.split("\r\n")[0].split(" ")
    
    stream_request = stream_path.findall(request_path)
    if(stream_request):
        stream_request  = stream_request[0]
        stream_request_type = stream_request[0]
        stream_id =  stream_request[1]
        
        
        if(stream_request_type=="events"):
            events_handler.add_listener(stream_id, socket)
            
        elif(stream_request_type=="audio_stream"):
            # periodically send data , most important
            handle_audio_stream(socket, address , stream_id)
            
        elif(stream_request_type=="init_data"):
            send_init_data(socket, address , stream_id)
            
            
        




if __name__ == "__main__":
    
    initDb()
    #initialize reading and file decoder
    #keep reading streams , auto reconnecting 
    stream_reader_thread = AudioStreamReader("telugu")
    stream_reader_thread.start()
    
    events_handler.start_reading_events()
    
    server = StreamServer(
    ('', 8888), handle_connection)
    server.serve_forever()    

