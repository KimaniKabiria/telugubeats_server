import urllib
from server.cookies import decode_signed_value
from models.user import User
from server.io_utils import response_write
from server.config import OK_404
import config

def user_auth(func):
    def new_func(socket , *args, **kwargs):
        query_params = kwargs.get("query_params")
        auth_key = query_params.get("auth_key")
        user = None
        if(auth_key):
            auth_key = urllib.unquote(auth_key[0])
            user_id = decode_signed_value(config.SERVER_SECRET,  "auth_key", auth_key)
            if(user_id):
                user = User.objects(pk=user_id)
            
        if(user):      
            user=user[0]
        else:
            user=None
            
        kwargs["user"]= user
        func(socket, *args, **kwargs)
        #installation_id = query_params.get("installation_id")
        
    return new_func

def user_auth_required(func):
    def new_func(socket , *args, **kwargs):
        query_params = kwargs.get("query_params")
        auth_key = query_params.get("auth_key")
        user = None
        if(auth_key):
            auth_key = urllib.unquote(auth_key[0])
            user_id = decode_signed_value(config.SERVER_SECRET ,"auth_key", auth_key)
            user = User.objects(pk=user_id)
            
        if(not user):
            response_write(socket, OK_404)
            return
        
        user=None
            
        kwargs["user"]= user
        func(socket, *args, **kwargs)
        #installation_id = query_params.get("installation_id")
        
    return new_func

