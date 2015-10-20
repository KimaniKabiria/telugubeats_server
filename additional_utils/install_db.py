from models import initDb
import json
from models.album import Album
from models.song import Song, SongsMeta
from models.polls import Poll
from mongoengine.document import Document

initDb()



def insert_init_data():
    
    Album.drop_collection()
    Song.drop_collection()
    
    
    data = json.loads(open("mapped_songs.json","r").read())
    count = 0
    for movie_name in data:
        movie = data[movie_name]
        a = Album()
        a.name = movie_name
        a.directors = movie.get("directors",None)
        a.music_directors = movie.get("music_directors",None)
        a.image_url = movie.get("img",None)
        a.actors = movie.get("actors",None)
        a.save()
        
        
        print "saved :: ", a.name
        for song_title_path  in  movie.get("song_entries",[]):
            if(not song_title_path): continue
            song_title , path  = song_title_path
            s = Song()
            s.title = song_title
#             s.lyricists = song.get("lyricists",None)
#             s.singers = song.get("singers",None)
            s.path = path
            s.album = a
            s.track_n = count
            count +=1
            s.save()
            print "    ", "saved song : " , s.title , s.album 
            
    
    poll = Poll.create_next_poll("telugu")
    print poll.to_json()
    print Poll.get_current_poll("telugu").to_json()        
    
    
    set_max_track()
    
def set_max_track():
    data = Song.objects().order_by("-track_n")[0]
    print data.track_n
    
    songsMeta = SongsMeta.objects().all()
    if(len(songsMeta)>0):
        m = songsMeta[0]
    else:
        m = SongsMeta()
    m.n = data.track_n
    m.save()


insert_init_data()

#get_max_track()