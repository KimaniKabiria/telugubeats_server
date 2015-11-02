import cStringIO
class BufferedFile(object):
    ''' A buffered file that preserves the beginning of a stream up to buffer_size
    '''
    def __init__(self, fp, buffer_size=1024*1024*10):
        self.data = cStringIO.StringIO()
        self.fp = fp
        self.offset = 0
        self.len = 0
        self.fp_offset = 0
        self.buffer_size = buffer_size

    @property
    def _buffer_full(self):
        return self.len >= self.buffer_size

    def readline(self):
        if self.len < self.offset < self.fp_offset:
            raise BufferError('Line is not available anymore')
        if self.offset >= self.len:
            line = self.fp.readline()
            self.fp_offset += len(line)

            self.offset += len(line)

            if not self._buffer_full:
                self.data.write(line)
                self.len += len(line)
        else:
            line = self.data.readline()
            self.offset += len(line)
        return line

    def seek(self, offset):
        if self.len < offset < self.fp_offset:
            raise BufferError('Cannot seek because data is not buffered here')
        self.offset = offset
        if offset < self.len:
            self.data.seek(offset)
            
            
            
def response_write(socket, data):
    n = 0
    l = len(data)
    while(n<l):
        n += socket.send(data[n:])
        if(n<0):
            break
        
