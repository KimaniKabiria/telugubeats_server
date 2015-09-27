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
gevent.monkey.patch_socket()

streaming_connections = {} #streamId : [connections]
stream_path = re.compile("/([^/]+)/(.+)")

#audio chunksize
stream_buffers = {
                  "telugu": [Buffer() , None]
}

    
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


def handle_events(socket, address , stream_id):
    pass

def handle_stream(socket, address, stream_id):    
    for i in config.RESPONSE:
        socket.send(i)
        print i
    # using a makefile because we want to use readline()
    buffer = stream_buffers[stream_id][0]
    last_sent_time = time.time() # 4 chunks once  #16*chunks per second #bitrate , 16kbytes per second =>
    current_index = buffer.get_current_head()-4
    
    while True:
        cur_time = time.time()
        if(cur_time - last_sent_time> 0.80):
            last_sent_time = cur_time
            chunk = buffer.get_chunk(current_index)
            #chunk = 32kb = > 16kbytes/sec => 1 chunks per 2 seconds 
            if(chunk):
                try:
                    n = 0
                    while(n<len(chunk)):    
                        n += socket.send(chunk[n:])
                    print "sending chunk at ", current_index , "writing unsynronized"
                    current_index+=1
                    gevent.sleep(0.80 - time.time()+last_sent_time)
                except:
                    #client disconnected
                    break
            else:
                gevent.sleep(0.80)
        else:
            print "waiting on buffer"
            gevent.sleep(1)
        

# this handler will be run for each incoming connection in a dedicated greenlet
def handle_connection(socket, address):
    print('New connection from %s:%s' % address)
    
    data = socket.recv(1024)
    request_type , request_path , http_version = data.split("\r\n")[0].split(" ")
    
    stream_request = stream_path.findall(request_path)
    if(stream_request):
        stream_request = stream_request[0]
        stream_id =  stream_request[1]

        if(stream_request[0]=="events"):
            handle_events(socket , address , stream_id)
        elif(stream_request[0]=="stream"):
            handle_stream(socket, address , stream_id)


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
            self.fd = open("/Users/abhinav/Downloads/bale_bale_magadivoy/04 - Motta Modatisari [www.AtoZmp3.in].mp3", 'rb')
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

