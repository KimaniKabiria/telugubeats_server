# 
# Author: Abhinav
#

import gevent.monkey
gevent.monkey.patch_socket()

import array
import gevent
from gevent.event import Event
from gevent.lock import Semaphore
import urllib
from additional_utils.urlutils import get_data



class RemoteUrlFileObject():
    sock_file = None
    file_buffer = None
    file_buffer_ptr = 0
    file_end_bool = False
    evt = None
    waiting_until = None
       
    def start_reading_dummy_bytes(self):
        byts = [1 for x in range(1024)]
        t = 1024
        while(byts):
            self.file_buffer.extend(byts)
            if(self.waiting_until!=None and len(self.file_buffer)>self.waiting_until):
                self.waiting_until = None
                self.evt.release()
                
            gevent.sleep(1)
            byts = [1 for x in range(1024)]
            t+=1024
        self.file_end_bool = True
        self.evt.release()
        
    
    def start_reading_bytes(self):
        try:
            byts = self.sock_file.read(1024)
            while(byts):
                self.file_buffer.extend(byts)
                if(self.waiting_until!=None and  len(self.file_buffer)>self.waiting_until):
                    print "read bytes :: ",len(self.file_buffer) , "releasing .."
                    self.waiting_until = None
                    self.evt.release()
                    
                byts = self.sock_file.read(1024)
        finally:
            self.file_end_bool = True
            self.evt.release()
                        
    
    def __init__(self, url):
        self.sock_file = get_data(url)
        gevent.spawn(self.start_reading_bytes)
        self.file_buffer = array.array('c')
        self.file_buffer_ptr = 0
#         gevent.spawn(self.start_reading_dummy_bytes)
        self.evt = Semaphore(value=0)
        
        
    def read(self, n_bytes):
        if(len(self.file_buffer) > self.file_buffer_ptr+n_bytes):
            bytes_until = self.file_buffer_ptr+n_bytes
            ret = self.file_buffer[self.file_buffer_ptr:  bytes_until]
            self.file_buffer_ptr = bytes_until
            return ret
        elif(self.file_end_bool):
            bytes_until = min(len(self.file_buffer) , self.file_buffer_ptr+n_bytes)
            ret = self.file_buffer[self.file_buffer_ptr:  bytes_until]
            self.file_buffer_ptr = bytes_until
            if(not ret):
                raise EOFError()
            return ret
        elif(not self.file_end_bool):# still reading in progress , wait on semaphore #block
            if(self.waiting_until!=None):
                print "cannot be called read while it's still blocked"
            self.waiting_until = self.file_buffer_ptr+n_bytes
            print "blocking."
            self.evt.acquire()#block
            return self.read(n_bytes)
        
        else:
            return None

    def sock_read(self, n_bytes):
        ret = []
        if(len(self.file_buffer) > self.file_buffer_ptr):
            bytes_until = min(len(self.file_buffer) , self.file_buffer_ptr+n_bytes)
            ret = self.file_buffer[self.file_buffer_ptr:  bytes_until]
            self.file_buffer_ptr = bytes_until
            return ret
        elif(self.file_end_bool):
            return None
        
    def seek(self, offset , from_what=0):
        if(len(self.file_buffer) > offset):
            self.file_buffer_ptr = offset
        else:#block until buffer is filled until offset
            print "blocking."
            self.waiting_until = offset
            self.evt.acquire()
            self.seek(offset)
            
    def close(self):
        try:
            self.sock_file.close()
        except:
            pass
        
def test():
    r = RemoteUrlFileObject("https://storage.googleapis.com/telugubeats_files/music/Telugu/others/sampangi%20%282001%29%20-%20%5B320%20-%20vbr%20-%20acd%20-%20tolymp3z%5D/sampangi.mp3")
    r.seek(1024)
    print r.read(1024)
    print r.read(1024)
    print r.read(1024)
    print r.read(1024)
    
    
if __name__ =='__main__':
    test()
    