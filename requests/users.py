from models.user import User
from bson import json_util
from helpers.auth import decode_signed_value, create_signed_value
from config import SERVER_SECRET, OK_200
import json
from responses.stream import InitData
from models.polls import Poll
from models.song import Song
from requests import stream_events_handler
from enums import Event
from gevent_handlers.events import EventListeners
from models import get_init_data
from helpers.io_utils import response_write

def do_register_user(socket, user=None, post = None):
    user = User.register_user(**json.loads(post["user_data"][0]))
    uid = str(user.id)
    user = user.to_son()
    print user
    user["auth_key"] = create_signed_value(SERVER_SECRET, "auth_key", uid)
    socket.send(OK_200)
    socket.send(json_util.dumps(user))
    socket.close()
    



def send_init_data(socket , stream_id, user=None):
    init_data = get_init_data(stream_id, user)
    init_data.last_few_events = EventListeners.last_few_events.get(stream_id, [])
    init_data = json_util.dumps(init_data.to_son())
    socket.send(OK_200)
    
    response_write(socket, init_data)
    
def do_dedicate_event(socket, stream_id,  post=None , user = None):
    user_name2 = post.get("user_name",["somebody"])
    stream_events_handler.publish_event(stream_id, Event.DEDICATE,  user_name2[0], from_user = user.to_short_mongo())
    
    socket.send(OK_200)
    socket.send("ok")
    socket.close()
    