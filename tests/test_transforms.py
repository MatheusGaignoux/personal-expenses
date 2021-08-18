from datetime import datetime
import sys
import os
import pytest
from os.path import dirname

path = dirname(dirname(os.path.abspath(__file__)))
sys.path.append(path + "/src")

from transforms import userTransform, expenseTransform

class TestUserTransform(object):
    def test_user_tranform(self):
        lastA = None
        lastB = {"income": 0, "state": 0}
        lastC = {"income": 0, "state": 0}
        dataA = {"username": "u.test", "name": "n.test"}
        dataB = {"username": "u.test", "name": "n.test", "income": 10000}
        dataC = {"username": "u.test", "name": "n.test", "income": 0}

        assert userTransform(0, lastA, dataA)["income"] == pytest.approx(0)
        assert userTransform(0, lastB, dataB)["income"] == pytest.approx(10000)
        assert userTransform(0, lastC, dataC) == None
    
class TestExpenseTransform(object):
    def test_expense_tranform(self):
        userId = 1
        eventType = "fix"
        chargedat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lastA = {"userid": userId, "fixexpenses": [], "varexpenses": []}
        dataA = {"expenseclass": "shopping", "amount": 1000.00, "chargedat": chargedat}

        result = expenseTransform(userId, eventType, lastA, dataA)

        assert result["fixexpenses"][-1]["id"] == pytest.approx(1)
        assert result["fixexpenses"][-1]["amount"] == pytest.approx(1000.00)
        assert result["eventtype"] == "fixexpenseinsertion"
