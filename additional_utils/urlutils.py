'''
@author: abhinav
'''

import urllib2
import logging
import zlib
from StringIO import StringIO
import hashlib
import os




from Queue import Queue
from threading import Thread

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


http_logger = urllib2.HTTPSHandler(debuglevel = 0)
url_loader=urllib2.build_opener(http_logger,urllib2.HTTPCookieProcessor(),urllib2.ProxyHandler())
urllib2.install_opener(url_loader)

def get_data(url,post=None,headers={}, method = None):
    headers['Accept-encoding'] ='gzip'
    ret= None
    try:
        req=urllib2.Request(url,post,headers)
        if(method!=None):
            req.get_method = lambda : method
        ret = url_loader.open(req) 
        if ret.info().get('Content-Encoding') == 'gzip':
            ret2 = ret
            try:
                ret = StringIO(zlib.decompress(ret2.read(),16+zlib.MAX_WBITS))
            except:
                decompressor = zlib.decompressobj()
                ret = StringIO(decompressor.decompress(ret2.read()))
            ret2.close()
            
    except urllib2.HTTPError, e: 
        print e
        ret = None
    return ret


def cache_and_get_data(url, post=None, headers={}, force = False , cache_folder_path="./cache/"):
    
    if(not os.path.exists(cache_folder_path)):
        os.makedirs(cache_folder_path)
    cache_file_path = cache_folder_path+hashlib.md5(url+(post[:7] if post else "")).hexdigest();
    if(os.path.isfile(cache_file_path) and not force):
        data = open(cache_file_path).read()
    else:
        conn = get_data(url, post, headers=headers)
        data = conn.read()
        f = open(cache_file_path,'w')
        f.write(data)
        f.close()
    return data