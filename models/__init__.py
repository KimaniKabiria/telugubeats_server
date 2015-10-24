from mongoengine.connection import connect
from mongoengine.document import Document




def initDb():
    dbServer = {"dbName":"telugubeats",
                       "ip":"104.155.234.161",# "db.quizapp.appsandlabs.com",
                       "port": 27017,
                       "username": "abhinav",
                       "password":"xxxxxxxx"
       }
    dbConnection = connect(dbServer["dbName"], host=dbServer["ip"], port=dbServer["port"], username=dbServer["username"],password=dbServer["password"])
    
    

class BaseNoOidDocument(object):
    def to_son(self,use_db_field=True, fields=None):
        data = Document.to_mongo(self, use_db_field=use_db_field, fields=fields)
        data["id"] = data["$oid"]
        del data["$oid"]
        return data