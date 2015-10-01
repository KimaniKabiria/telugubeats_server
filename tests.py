from models.album import Album
from server import initDb
from models.song import Song
import json
from bson.son import SON
import bson
from bson import json_util


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
    data["song"] = song.to_mongo()
    print json_util.dumps(data)
    

test2()