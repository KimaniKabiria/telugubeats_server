server_address = '0.0.0.0'
server_port = 8888



SERVER_SECRET = "ubjebkhelloworlddudemomiloveyou"
CHUNKSIZE = 32*1024# 417 bytes=one frame = 1152 samples, 39frames per second , 



OK_200 = "HTTP/1.0 200 OK\r\n\r\n"

RESPONSE = ["HTTP/1.0 200 OK\r\n",
     "icy-notice1: <BR>This stream requires",
     "icy-notice2: Winamp, or another streaming media player<BR>\r\n",
     "icy-name: Python mix\r\n",
     "icy-genre: Jazz Classical Rock\r\n",
     "icy-url: http://", server_address, ":", str(server_port), "\r\n",
     "content-type: audio/mpeg\r\n",
     "icy-pub: 1\r\n",
     "icy-metaint: ", str(CHUNKSIZE), "\r\n",
     "icy-br: 128\r\n",
     "ice-audio-info: ice-samplerate=44100;ice-bitrate=128;ice-channels=2\r\n",
     "icy-br: 128\r\n\r\n"]