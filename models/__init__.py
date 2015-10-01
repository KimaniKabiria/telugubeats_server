from mongoengine.connection import connect




def initDb():
    dbServer = {"dbName":"quizApp",
                       "ip":"0.0.0.0",# "db.quizapp.appsandlabs.com",
                       "port": 27017,
                       "username": "quizapp",
                       "password":"XXXXX"
       }
    dbConnection = connect(dbServer["dbName"], host=dbServer["ip"], port=dbServer["port"])
    