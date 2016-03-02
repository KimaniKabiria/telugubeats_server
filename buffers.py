class Buffer():
#     SIZE  = 2*1024 # no of blocks , that contain chunks 32 MB
#     CHUNK_BYTE_SIZE = 32*1024 # 32kb
#     _byte_chunks = [0 for i in range(SIZE)]
    size  = None
    chunk_byte_size = None
    _byte_chunks = None
    h = 0
    b = 0 # from back till h    
    
    def __init__(self , size=2*1024, chunk_byte_size=32*1024):
        self.size = size
        self.chunk_byte_size = chunk_byte_size
        self._byte_chunks = [0 for i in range(size)]
    
    def queue_chunk(self, _bytes):
        self._byte_chunks[self.h%self.size] = _bytes
        self.h = (self.h+1)%self.size
    
    def deque_chunk(self):
        data = self._byte_chunks[self.b]
        self.b+=1
        self.b%=self.size
        return data
        
    def is_available(self):
        return self.h!=self.b
    
    def size(self):
        return abs(self.h-self.b)

    def get_chunk(self, index):# no size check
        return self._byte_chunks[index%self.size]
    
    def get_current_head(self):
        return self.h-1
    
    def get_past_data_index(self):
        return (self.h- 256 + self.size)%self.size # 256 seconds approx 