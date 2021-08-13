from flask import Flask
from flask_restful import Api
from user import UserAuth, UserIncome

app = Flask(__name__)
app.secret_key = "matheus"
api = Api(app)

api.add_resource(UserAuth, "/users/register")
api.add_resource(UserIncome, "/users/<string:username>/args")

app.run(debug = False, host = "0.0.0.0", port = 5001)