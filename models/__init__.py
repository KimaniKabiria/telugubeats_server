from mongoengine.connection import connect
from mongoengine.document import Document
from models.song import Song
from models.polls import Poll
from responses.stream import InitData




def initDb():
    dbServer = {"dbName":"telugubeats",
                       "ip":"104.155.234.161",# "db.quizapp.appsandlabs.com",
                       "port": 27017,
                       "username": "abhinav",
                       "password":"xxxxx"
       }
    dbConnection = connect(dbServer["dbName"], host=dbServer["ip"], port=dbServer["port"], username=dbServer["username"],password=dbServer["password"])
    
    

class BaseNoOidDocument(object):
    def to_son(self,use_db_field=True, fields=None):
        data = Document.to_mongo(self, use_db_field=use_db_field, fields=fields)
        data["id"] = data["$oid"]
        del data["$oid"]
        return data
    
    
    
def get_init_data(stream_id, user=None):
    from requests import stream_events_handler
    song = Song.objects().order_by("-last_played")[0]
    
    poll = Poll.get_current_poll(stream_id)
    
    init_data = InitData()
    if(user):
        init_data.user = user
        poll_item = user.get_poll_item(poll)
        if(poll_item):
            init_data.user_poll_item_id = str(poll_item.id)#string
        
    init_data.poll = poll
    init_data.n_user = len( stream_events_handler.event_listeners[stream_id])
    init_data.current_song  = song
    
    return init_data