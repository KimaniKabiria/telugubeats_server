from mongoengine.connection import connect
from mongoengine.document import Document
from models.song import Song
from models.polls import Poll
from responses.stream import InitData


    

class BaseNoOidDocument(object):
    def to_son(self,use_db_field=True, fields=None):
        data = Document.to_mongo(self, use_db_field=use_db_field, fields=fields)
        data["id"] = data["$oid"]
        del data["$oid"]
        return data
    
    
    
