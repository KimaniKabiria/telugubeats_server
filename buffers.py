
class Buffer():
    SIZE  = 2*1024 # no of blocks , that contain chunks 2 MB
    CHUNK_BYTE_SIZE = 32*1024 # 32kb
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