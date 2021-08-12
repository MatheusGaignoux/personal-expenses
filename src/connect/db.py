import pymongo as mongo
import yaml
import os

path = os.path.dirname(os.path.realpath(__file__))  

with open(path + "/config.yaml", "r") as file:
    config = yaml.load(file, Loader = yaml.FullLoader)

class Nosql:
    global config
    __conn = mongo.MongoClient(**config["Mongo"]["MongoConfig"])

    @classmethod
    def conn(cls):
        return cls.__conn[config["Mongo"]["db"]]
    
    def last(self, collectionConnection, username):
        return collectionConnection.find_one(filter = {"user": username}, sort = [("datetime", -1)])

    def lastUserId(self, collectionConnection):
        return collectionConnection.find_one(projection = ["userid"], sort = [("userid", -1)])["userid"]