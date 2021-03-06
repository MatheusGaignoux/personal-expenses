from flask_restful import Resource, reqparse
from connect.db import Nosql
from datetime import datetime

class UserEntryPoint:
    def getConnection(self):
        self.entrypoint = Nosql()
        self.collection = self.entrypoint.conn()["users"]

    @classmethod
    def transform(cls, id, last, data):
        if last is None:
            income = data.get("income", 0)
            values = (income, 0, "usercreation")

        elif data.get("income") and last.get("income", 0) != data.get("income", 0):
            values = (data["income"], last["state"] + 1, "incomeuptade")

        else:
            return None

        data["userid"] = id
        data["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        doc = dict(list(data.items()) + list(zip(("income", "state", "eventtype"), values)))

        return doc

class UserPack:
    __parser = reqparse.RequestParser()
    __parser.add_argument("name", required = True, type = str)
    __parser.add_argument("username", required = True, type = str)
    
    @classmethod
    def parser(cls):
        return cls.__parser

class UserAuth(Resource, UserEntryPoint):
    def __init__(self):
        self.getConnection()
        self.__parser = UserPack.parser()
        self.__parser.add_argument("income", required = False, type = float)

    def post(self):
        data = self.__parser.parse_args()
        last = self.entrypoint.last(self.collection, data["username"])

        if last is None:
            lastUserId = self.entrypoint.lastUserId(self.collection)
            
            doc = UserEntryPoint.transform(lastUserId.get("userid", 0) + 1 if lastUserId else 0, last, data)
            self.entrypoint.insert(self.collection, doc)

            return  doc, 201
        else:
            message = "username {} already in use".format(data["username"])
            return {"message": message}, 400

class UserIncome(Resource, UserEntryPoint):
    def __init__(self):
        self.getConnection()
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument("income", required = True, type = float)

    def put(self, username):
        data = self.__parser.parse_args()
        last = self.entrypoint.last(self.collection, username)
        if last:
            data["name"] = last["name"]
            data["username"] = username
            
            doc = UserEntryPoint.transform(last["userid"], last, data)
            
            if doc:
                self.entrypoint.insert(self.collection, doc)

            return (doc, 201) if doc else ({"message": "last state not changed"}, 400)
        
        return {"message": "username {} inexists".format(username)}, 404

    def get(self, username):
        last = self.entrypoint.last(self.collection, username)
        last.pop("_id")
        return {"last": last}, 201
