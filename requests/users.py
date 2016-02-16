from models.user import User
from bson import json_util
from server.cookies import decode_signed_value, create_signed_value
from config import SERVER_SECRET, OK_200
import json
from models.polls import Poll
from models.song import Song
from enums import Event
from server.io_utils import response_write
from handlers.streams import streams
from utils import user_auth


@user_auth
def do_register_user(socket, user=None, query_params=None):
    user = User.register_user(**json.loads(query_params["user_data"][0]))
    uid = str(user.id)
    user = user.to_son()
    print user
    user["auth_key"] = create_signed_value(SERVER_SECRET, "auth_key", uid)
    socket.send(OK_200)
    socket.send(json_util.dumps(user))
    socket.close()
    

@user_auth
def do_dedicate_event(socket, stream_id, query_params=None, user = None):
    user_name2 = query_params.get("user_name",["somebody"])
    streams.get(stream_id).publish_event(Event.DEDICATE,  user_name2[0], from_user = user.to_short_son())
    
    socket.send(OK_200)
    socket.send("ok")
    socket.close()
    

@user_auth
def get_current_user(socket,query_params=None, user=None):
    response_write(socket, OK_200)
    if(user):
        uid = str(user.id)
        user = user.to_son()
        user["auth_key"] = create_signed_value(SERVER_SECRET, "auth_key", uid)
        response_write(socket, json_util.dumps(user))
    socket.close()
    