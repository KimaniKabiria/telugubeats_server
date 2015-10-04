from models.album import Album
from server import initDb
from models.song import Song
import json
from bson.son import SON
import bson
from bson import json_util
import socket
from StringIO import StringIO
from models.polls import Poll


initDb()
    
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

def test4():
    ''' poll create and get one'''
#    initDb()
    poll = Poll.create_next_poll("telugu")
    print poll.to_json()
    print Poll.get_current_poll("telugu").to_json()
    
test4()
    
test3()