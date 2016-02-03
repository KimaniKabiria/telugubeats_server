'''
Created on Oct 9, 2015

@author: abhinav
'''
from enums import Event
from config import OK_200
from handlers.streams import streams

def do_chat_event(socket,stream_id , post=None , user=None):
    message = post.get("chat_message",None)
    if(message):
        streams.get(stream_id).publish_event(Event.CHAT_MESSAGE,  message[0], from_user = str(user.id))
    
    socket.send(OK_200)
    socket.send("ok")
    socket.close()