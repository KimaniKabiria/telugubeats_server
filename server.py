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
gevent.monkey.patch_socket()

streaming_connections = {} #streamId : [connections]

    




class Buffer():
    SIZE  = 100*1024 # no of blocks , that contain chunks 100 MB
    CHUNK_BYTE_SIZE = 32*1024
    _byte_chunks = [0 for i in range(SIZE)]
    h = 0
    b = 0 # from back till h    
    def queue_chunk(self, _bytes):
        self._byte_chunks[self.h%Buffer.SIZE] = _bytes
        self.h = (self.h+1)%Buffer.SIZE
    
    def deque_chunk(self):
        data = self._byte_chunks[self.b]
        self.b+=1
        self.b%=Buffer.SIZE
        
    def is_available(self):
        return self.h!=self.b
    
    def size(self):
        return abs(self.h-self.b)

    def get_chunk(self, index):
        if(self.size()>0) :  
            return self._byte_chunks[index]
        return None
    
    def get_current_head(self):
        return self.h-1

#audio chunksize
stream_buffers = {
                  "telugu": [Buffer() , None]
         }

class StreamingClient():
    current_index = 0
    last_sent_time = 0
    buffer = None
    socket = None
    last_sent_time = time.time() # 4 chunks once  #16*chunks per second #bitrate , 16kbytes per second =>
    stream_id = None
    
    def __init__(self, stream_id):
        self.stream_id = stream_id
        self.buffer = stream_buffers[stream_id][0]
        streaming_connections[self.stream_id].append(self)
        
    def handle_write(self):# should call whenever socket is writable , continuously call this method
        if(time.time() - self.last_sent_time > 0.25):
            for i in range(4):
                chunk = self.buffer.get_chunk(self.current_index)
                if(chunk):
                    self.socket.send(chunk)
                    self.current_index+=1
            self.last_sent_time = time.time()
    
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



def get_next_file():# from the current polls
    pass


def create_polls():
    pass

#@celient_session
def listen_to_audio_stream( stream_id ,  user =None):
    pass

#@client_session
def listen_to_general_events(stream_id , user =None):
    pass

def get_next_polls(stream_id):
    pass


event_path = re.compile("/([^/]+)/(.+)")




def audio_streaming(socket, address , stream_id):
    
    
    for i in config.RESPONSE:
        socket.send(i)
        print i
    # using a makefile because we want to use readline()
    buffer = stream_buffers["telugu"][0]
    last_sent_time = time.time() # 4 chunks once  #16*chunks per second #bitrate , 16kbytes per second =>
    current_index = buffer.get_current_head()-4
    
    while True:
        cur_time = time.time()
        if(cur_time - last_sent_time> 0.80):
            last_sent_time = cur_time
            chunk = buffer.get_chunk(current_index)
            #chunk = 32kb = > 16kbytes/sec => 1 chunks per 2 seconds 
            if(chunk):
                socket.send(chunk)
                print "sending chunk at ", current_index , "writing unsynronized"
                current_index+=1
                gevent.sleep(0.80 - time.time()+last_sent_time)
            else:
                gevent.sleep(0.80)
        else:
            print "waiting on buffer"
            gevent.sleep(1)
        


# this handler will be run for each incoming connection in a dedicated greenlet
def handle_connection(socket, address):
    print('New connection from %s:%s' % address)
    
    data = socket.recv(1024)
    headers = data.split("\r\n")
    request_type , request_path , http_version = headers[0].split(" ")
    
    request_path = event_path.findall(request_path)
    
    if(request_path):
        stream_id =  request_path[0]
#         send_events(socket , address , stream_id)
        return
    else:
        stream_


class AudioStreamReader(Greenlet):
    stream_id = None
    fd = None
    id3 = None
    last_time_stamp  = time.time()

    # write to telugu buffer
    def __init__(self, stream_id):
        Greenlet.__init__(self)
        self.stream_id = stream_id
        self.buffer = stream_buffers[self.stream_id][0]
    def _run(self):
        while(True):
            self.fd = open("/Users/abhinav/Downloads/bale_bale_magadivoy/02 - Endaro [www.AtoZmp3.in].mp3", 'rb')
            print self.fd
            # if there is valid ID3 data, read it out of the file first,
            # so we can skip sending it to the client
            try:
                self.id3 = id3reader.Reader(self.fd)
                if isinstance(self.id3.header.size, int): # read out the id3 data
                    self.fd.seek(self.id3.header.size, os.SEEK_SET)
                
                while(True):
                    try:
                        cur_time = time.time()
                        if(cur_time- self.last_time_stamp > 0.80):
                            self.last_time_stamp = cur_time
                            data_arr = array.array('B')
                            data_arr.fromfile(self.fd, Buffer.CHUNK_BYTE_SIZE)
                            self.buffer.queue_chunk(data_arr)
                            print "writing data into stream buffer , queued chuck", self.buffer.get_current_head() 
                            gevent.sleep(0.80- time.time()+self.last_time_stamp)
                    except EOFError:
                        self.fd.close()
                        break        
            except Exception as e:
                    print e

if __name__ == "__main__":
    
    #initialize reading and file decoder
    stream_reader_thread = AudioStreamReader("telugu")
    stream_reader_thread.start()
    
    server = StreamServer(
    ('', 8888), handle_connection)
    server.serve_forever()    

