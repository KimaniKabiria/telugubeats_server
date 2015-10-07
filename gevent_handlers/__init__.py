from gevent_handlers.audio_streams import AudioStreamReader


#initialize stream reader

def init_main_audio_streams():
    stream_reader_thread = AudioStreamReader("telugu")
    stream_reader_thread.start()



    
    