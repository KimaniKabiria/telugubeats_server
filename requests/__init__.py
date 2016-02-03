from helpers.io_utils import response_write
from bson import json_util
import json
from config import OK_200
from handlers.streams import streams


## stream requesats init


    
def print_stats(socket, stream_id="telugu", user = None):
    live_sockets = streams.get(stream_id).event_listeners
    stats = {"live users : ":map(lambda x : {x: len(live_sockets[x])} , live_sockets.keys())}
    html = '''<html>
        <body>
        <div><b>Live Users : </b>&nbsp;&nbsp;&nbsp;&nbsp;'''+json.dumps(stats,indent=4)+'''</div>
        </body>
    </html>'''
    socket.send(OK_200)
    response_write(socket, html)
    socket.close()
    