'''
Created on Oct 3, 2015

@author: abhinav
'''
from requests import stream_events_handler
from responses.polls import PollChangeEvent
from enums import Event
from config import OK_200


def do_poll(socket, stream_id, poll_id, poll_item_id, user = None):
    old_poll_item_id, old_song_title, new_poll_id , new_song_title = user.do_poll(poll_id, poll_item_id)
    
    # do events
    if(old_poll_item_id!=poll_item_id):
        changes = [PollChangeEvent(poll_id = poll_item_id , count = 1, song_title= new_song_title)]
        if(old_poll_item_id!=None):
            changes.append(PollChangeEvent(poll_id = old_poll_item_id , count = -1 , song_title=old_song_title))
            
        p = PollChangeEvent.get_poll_changes_to_json(changes)
        stream_events_handler.publish_event(stream_id, Event.POLL_CHANGES,  p, from_user = user.to_short_mongo())

    socket.send(OK_200)
    socket.send("ok")
    socket.close()
    