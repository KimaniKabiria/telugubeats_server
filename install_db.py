from models import initDb
import json
from models.album import Album
from models.song import Song, SongsMeta

initDb()

def insert_init_data():
    data = json.loads(open("song_data.json","r").read())
    count = 0
    for movie_name in data:
        movie = data[movie_name]
        a = Album()
        a.name = movie_name
        a.directors = data.get("directors",None)
        a.music_directors = data.get("music_directors",None)
        a.imageUrl = data.get("img",None)
        a.actors = data.get("actors",None)
        a.save()
        print "saved :: ", a.name
        for song in movie.get("songs",[]):
            s = Song()
            s.title = song.get("name",None)
            s.lyricists = song.get("lyricists",None)
            s.singers = song.get("singers",None)
            s.album = a
            s.track_n = count
            count +=1
            s.save()
            print "    ", "saved song : " , s.title        
            
def get_max_track():
    data = Song.objects().order_by("-track_n")[0]
    print data.track_n
    m = SongsMeta()
    m.n = data.track_n
    m.save()
    
    
    
get_max_track()