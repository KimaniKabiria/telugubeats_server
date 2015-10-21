

import array
import gevent
from gevent.event import Event
from gevent._threading import Semaphore



class RemoteUrlFileObject():
    sock_file = None
    file_buffer = array.array('B')
    file_buffer_ptr = 0
    file_end_bool = False
    evt = None
    waiting_until = None
       
    def start_reading_dummy_bytes(self):
        byts = [1 for x in range(1024)]
        t = 1024
        print "started loading dummy bytes"
        while(byts):
            self.file_buffer.extend(byts)
            if(self.waiting_until!=None and len(self.file_buffer)>self.waiting_until):
                self.waiting_until = None
                print "releasing lock"
                self.evt.release()
                
            print "reading 1024 bytes", "read: ", len(self.file_buffer)
            gevent.sleep(1)
            byts = [1 for x in range(1024)]
            t+=1024
        self.file_end_bool = True
        self.evt.release()
        
    
    def start_reading_bytes(self):
        byts = self.sock_file.read(1024)
        while(byts):
            self.file_buffer.extend(byts)
            if(self.waiting_until!=None and  len(self.file_buffer)>self.waiting_until):
                self.waiting_until = None
                self.evt.release()
                
            print "reading 1024 bytes", "read: ", len(self.file_buffer)
            byts = self.sock_file.read(1024)
        self.file_end_bool = True
        self.evt.release()
                        
    
    def __init__(self, url):
#         self.sock_file = urllib.urlopen(url)
#         gevent.spawn(self.start_reading_bytes, self)
#         self.evt = Event()
        gevent.spawn(self.start_reading_dummy_bytes)
        self.evt = Semaphore(value=0)
        
        
    def read(self, n_bytes):
        print "a"
        if(len(self.file_buffer) > self.file_buffer_ptr+n_bytes):
            print "b"
            bytes_until = self.file_buffer_ptr+n_bytes
            ret = self.file_buffer[self.file_buffer_ptr:  bytes_until]
            self.file_buffer_ptr = bytes_until
            return ret
        elif(self.file_end_bool):
            print "c"
            bytes_until = min(len(self.file_buffer) , self.file_buffer_ptr+n_bytes)
            ret = self.file_buffer[self.file_buffer_ptr:  bytes_until]
            self.file_buffer_ptr = bytes_until
            return ret
        elif(not self.file_end_bool):# still reading in progress , wait on semaphore #block
            print "d"
            if(self.waiting_until!=None):
                print "cannot be called read while it's still blocked"
            self.waiting_until = self.file_buffer_ptr+n_bytes
            self.evt.acquire()#block
            print "block ? passed"
            return self.read(n_bytes)
        
        else:
            print "e"
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
        
    def seek(self, offset):
        if(len(self.file_buffer) > offset):
            self.file_buffer_ptr = offset
        else:#block until buffer is filled until offset
            self.waiting_until = offset
            self.evt.acquire()
            self.seek(offset)

def test():
    r = RemoteUrlFileObject(None)
    print r.read(1024)
    print r.read(1024)
    print r.read(1024)
    print r.seek(1024)
    print r.read(1024)
    
    
if __name__ =='__main__':
    test()
    