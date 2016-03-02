from models.album import Album
from models.song import Song
import json
from bson.son import SON
import bson
from bson import json_util
import socket
from StringIO import StringIO
from models.polls import Poll, UserPolls
from mongoengine.document import Document
from mongoengine.fields import ReferenceField, IntField
from bson.dbref import DBRef
import array
import buffers



    
def load():
    album = Album()
    album.name = "100 Kotlu"
    album.actors = [
            "Krishna", 
            "Baladitya", 
            "Syerabhanu", 
            "Brahmanandam"
        ]
    album.music_directors = ["Vandemataram Srinivas"]
    album.directors = ["maruthi"]
    album.imageUrl = "http://rgamedia.blob.core.windows.net/raagaimg/r_img/catalog/cd/a/a0001232.jpg"
    album.save()
    
    print album.to_json()
    
    song = Song()
    
    song.album = album
    song.title = "Chirunayyu"
    song.genre  = None
    
    song.lyricists = [
                    "Surisetty Ramarao"
                ]
    
    song.singers =  [
                    "Malathi"
                ]
    song.rating = 10
    song.save()
    
    print song.to_json()
    
def test2():
    song = Song.objects().get()
    data = SON()
    data["song"] = song.to_son()
    print json_util.dumps(data)

def test3():
    from mimetools import Message
    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to a public host,
    # and a well-known port
    serversocket.bind(("0.0.0.0", 8886))
    #become a server socket
    serversocket.listen(5)
    while 1:
        #accept connections from outside
        (clientsocket, address) = serversocket.accept()
        #now do something with the clientsocket
        #in this case, we'll pretend this is a threaded server
        request_text =  clientsocket.recv(1<<16)
        print "###" , post_data

def test4(create_poll=False):
    ''' poll create and get one'''
#    initDb()
    if(create_poll):
        poll = Poll.create_next_poll("telugu")
        print poll.to_json()
    print Poll.get_current_poll("telugu").to_json()
    
 
def test5():
    class B(Document):
        count = IntField()
        
    class A(Document):
        b = ReferenceField(B)
        
    
    b = B(count =100)
    b.save()
    a = A(b = DBRef('B', b.id))
    a.save()
    print a.to_json() , b.to_json()
    
    print "###", a.id  , b.id
    print type(b.id)
    print A.objects(b =  b.id).get().to_json()
    

def test_6():
    #save in db offlise for create_next_poll
    initDb()
    poll = Poll.create_next_poll("telugu", False)
    print poll
    print json_util.dumps(poll.to_son())
    
def test_7():
    #random , test id , mongo field
    initDb()
    poll = Poll.get_current_poll("telugu")
    print str(poll.poll_items[0].id)
    print json_util.dumps(poll.poll_items[0].id)
    print json_util.dumps(poll.poll_items[0].poll.id)
    
    
    
def test_8():
    b = buffers.Buffer(10 , 1)
    b.size = 10
    b.chunk_byte_size = 1
    for i in range(1,20):
        b.queue_chunk(i)
        print b._byte_chunks
    
    
    
def test_9():
    from server.cookies import decode_signed_value, create_signed_value
    import urllib
    import config
    
    user_key = create_signed_value(config.SERVER_SECRET, "auth_key", "56cb16c247120d6c14888a26")
    print urllib.quote(user_key)
    print decode_signed_value(config.SERVER_SECRET , "auth_key",urllib.unquote(user_key))

        
#test4(False)
test_9()   
