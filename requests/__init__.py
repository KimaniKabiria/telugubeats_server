from gevent_handlers.events import EventListeners
from helpers.io_utils import response_write
from bson import json_util
import json
from config import OK_200


## stream requesats init
stream_events_handler = EventListeners()



def init_stream_event_handlers():
    stream_events_handler.init_stream_listeners("telugu")
    
    
def print_stats(socket, user = None):
    live_sockets = stream_events_handler.event_listeners
    stats = {"live users : ":map(lambda x : {x: len(live_sockets[x])} , live_sockets.keys())}
    html = '''<html>
        <body>
        <div><b>Live Users : </b>&nbsp;&nbsp;&nbsp;&nbsp;'''+json.dumps(stats,indent=4)+'''</div>
        </body>
    </html>'''
    socket.send(OK_200)
    response_write(socket, html)
    