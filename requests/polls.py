'''
Created on Oct 3, 2015

@author: abhinav
'''
from responses.polls import PollChangeEvent
from enums import Event
from config import OK_200
from helpers.io_utils import response_write
from models.polls import Poll
from bson import json_util
from handlers.streams import streams


def do_poll(socket, stream_id, poll_id, poll_item_id, user = None):
    old_poll_item_id, old_song_title, new_poll_id , new_song_title = user.do_poll(poll_id, poll_item_id)
    
    stream = streams.get(stream_id)
    
    # do events
    if(old_poll_item_id!=poll_item_id):
        changes = [PollChangeEvent(poll_id = poll_item_id , count = 1, song_title= new_song_title)]
        if(old_poll_item_id!=None):
            changes.append(PollChangeEvent(poll_id = old_poll_item_id , count = -1 , song_title=old_song_title))
            
        p = PollChangeEvent.get_poll_changes_to_json(changes)
        stream.publish_event(Event.POLLS_CHANGED,  p, from_user = user)

    socket.send(OK_200)
    socket.send("ok")
    socket.close()
    

def get_current_poll(socket, stream_id, user=None):
    response_write(socket, OK_200)
    response_write(socket, json_util.dumps(Poll.get_current_poll(stream_id).to_son()))
    socket.close()
    
def get_poll_by_id(socket, poll_id, user=None):
    response_write(socket, OK_200)
    response_write(socket, json_util.dumps(Poll.objects(pk=poll_id).get().to_son()))
    socket.close()