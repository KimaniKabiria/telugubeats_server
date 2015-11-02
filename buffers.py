
class Buffer():
    SIZE  = 2*512 # no of blocks , that contain chunks 32 MB
    CHUNK_BYTE_SIZE = 32*1024 # 32kb
    _byte_chunks = [0 for i in range(SIZE)]
    h = 0
    b = 0 # from back till h    
    def queue_chunk(self, _bytes):
        self._byte_chunks[self.h%self.SIZE] = _bytes
        self.h = (self.h+1)%self.SIZE
    
    def deque_chunk(self):
        data = self._byte_chunks[self.b]
        self.b+=1
        self.b%=self.SIZE
        return data
        
    def is_available(self):
        return self.h!=self.b
    
    def size(self):
        return abs(self.h-self.b)

    def get_chunk(self, index):# no size check
        return self._byte_chunks[index%self.SIZE]
    
    def get_current_head(self):
        return self.h-1