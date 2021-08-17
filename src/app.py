from flask import Flask
from flask_restful import Api
from user import UserAuth, UserIncome
from expenses import Expenses, FixExpense

app = Flask(__name__)
app.secret_key = "matheus"
api = Api(app)

api.add_resource(UserAuth, "/users/register")
api.add_resource(UserIncome, "/users/<string:username>/args")
api.add_resource(FixExpense, "users/<string:username>/expenses/fixexpense")
api.add_resource(Expenses, "/users/<string:username>/expenses")

app.run(debug = False, host = "0.0.0.0", port = 5001)