from bson import json_util
import json
from config import OK_200
from handlers.streams import streams
from utils import user_auth
from server.io_utils import response_write


## stream requesats init


@user_auth
def print_stats(socket, stream_id="telugu", user = None):
    live_sockets = streams
    stats = {"live users : ":map(lambda x : {x: len(live_sockets[x].event_listeners)} , live_sockets.keys())}
    html = '''<html>
        <body>
        <div><b>Live Users : </b>&nbsp;&nbsp;&nbsp;&nbsp;'''+json.dumps(stats,indent=4)+'''</div>
        </body>
    </html>'''
    socket.send(OK_200)
    response_write(socket, html)
    socket.close()
    