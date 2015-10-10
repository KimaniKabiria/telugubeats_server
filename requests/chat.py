'''
Created on Oct 9, 2015

@author: abhinav
'''
from enums import Event
from requests import stream_events_handler
from config import OK_200

def do_chat_event(socket,stream_id , post=None , user=None):
    message = post.get("chat_message",["-"])
    stream_events_handler.publish_event(stream_id, Event.CHAT_MESSAGE,  message[0], from_user = user.to_short_mongo())
    
    socket.send(OK_200)
    socket.send("ok")
    socket.close()