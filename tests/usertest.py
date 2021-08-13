import sys
import os
import pytest
from os.path import dirname

path = dirname(dirname(os.path.abspath(__file__)))
sys.path.append(path + "/src")

from user import UserEntryPoint as ep

def test_tranform_user_data():
    lastA = None
    lastB = {"income": 0, "state": 0}
    lastC = {"income": 0, "state": 0}
    dataA = {"username": "u.test", "name": "n.test"}
    dataB = {"username": "u.test", "name": "n.test", "income": 10000}
    dataC = {"username": "u.test", "name": "n.test", "income": 0}

    assert ep.transform(0, lastA, dataA)["income"] == pytest.approx(0)
    assert ep.transform(0, lastB, dataB)["income"] == pytest.approx(10000)
    assert ep.transform(0, lastC, dataC)["income"] == None