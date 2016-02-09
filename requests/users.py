from models.user import User
from bson import json_util
from helpers.auth import decode_signed_value, create_signed_value
from config import SERVER_SECRET, OK_200
import json
from models.polls import Poll
from models.song import Song
from enums import Event
from helpers.io_utils import response_write
from handlers.streams import streams

def do_register_user(socket, user=None, post = None):
    user = User.register_user(**json.loads(post["user_data"][0]))
    uid = str(user.id)
    user = user.to_son()
    print user
    user["auth_key"] = create_signed_value(SERVER_SECRET, "auth_key", uid)
    socket.send(OK_200)
    socket.send(json_util.dumps(user))
    socket.close()
    

    
def do_dedicate_event(socket, stream_id,  post=None , user = None):
    user_name2 = post.get("user_name",["somebody"])
    streams.get(stream_id).publish_event(Event.DEDICATE,  user_name2[0], from_user = user.to_short_son())
    
    socket.send(OK_200)
    socket.send("ok")
    socket.close()
    
def get_current_user(socket, user=None):
    socket.send(OK_200)
    if(user):
        uid = str(user.id)
        user = user.to_son()
        user["auth_key"] = create_signed_value(SERVER_SECRET, "auth_key", uid)
        socket.send(json_util.dumps(user))
    socket.close()
    