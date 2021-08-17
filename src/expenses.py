from flask_restful import Resource, reqparse
from connect.db import Nosql
from tranforms import transformExpense

class ExpensePack:
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument("expenseclass", required = True, type = str)
        self.__parser.add_argument("value", required = True, type = float)
        self.__parser.add_argument("chargedat", required = True, type = str)

    def parser(self):
        return self.__parser

class FixExpense(Resource):
    def __init__(self):
        self.__entrypoint = Nosql()
        self.__conn = self.__entrypoint.conn()
        self.__parser = ExpensePack().parser()
        self.__parser.add_argument("paidat", required = False, type = str)
        self.__parser.add_argument("partnumber", required = False, type = int)
        self.__parser.add_argument("amortization", required = False, type = float)

    def post(self, username):
        data = self.__parser.parse_args()
        
        userData = self.__entrypoint.last(self.__conn["users"], username)
        lastData = self.__entrypoint.last(self.__conn["expenses"], username)

        if userData:
            id = userData["userid"]

class Expenses(Resource):
    def __init__(self):
        self.__entrypoint = Nosql()
        self.__conn = self.__entrypoint.conn()

    def get(self, username):
        result = self.__entrypoint.last(self.__conn["users"], username)
        userid = result["userid"] if result else None

        if userid:
            msg = self.__entrypoint.historic(self.__conn["expenses"], userid)
            return {"payload": msg}, 201

        return {"message": "inexistent username {}".format(username)}, 400
        