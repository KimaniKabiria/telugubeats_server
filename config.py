server_address = '0.0.0.0'
server_port = 8888


db_server = {"db_name":"telugubeats",
                   "host":"localhost",# "db.quizapp.appsandlabs.com",
                   "port": 27017,
                   "user_name": "abhinav",
                   "password":""
   }




host_id = None

SERVER_SECRET = "ubjebkhelloworlddudemomiloveyou"
CHUNKSIZE = 32*1024# 417 bytes=one frame = 1152 samples, 39frames per second , 

IS_TEST_BUILD = True

OK_200 = "HTTP/1.0 200 OK\r\n\r\n"

RESPONSE = ["HTTP/1.0 200 OK\r\n",
     "icy-notice1: <BR>This stream requires",
     "icy-notice2: Winamp, or another streaming media player<BR>\r\n",
     "icy-name: Python mix\r\n",
     "icy-genre: Jazz Classical Rock\r\n",
     "icy-url: http://", server_address, ":", str(server_port), "\r\n",
     "content-type: audio/mpeg\r\n",
     "Pragma: no-cache",
     "Cache-Control: no-cache",
     "icy-pub: 0\r\n",
#     "icy-metaint: ", str(CHUNKSIZE), "\r\n",
     "icy-br: 128\r\n",
     "ice-audio-info: ice-samplerate=44100;ice-bitrate=128;ice-channels=2\r\n",
     "icy-br: 128\r\n\r\n"]