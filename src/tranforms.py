from datetime import datetime

def transformUser(userid, last, data):
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

def transformExpense(userid, expenseType = None, last = {}, data = {}):
    doc = last.copy()

    if last:
        expenseId = last[expenseType + "expenses"][-1]["id"] + 1 if last[expenseType + "fixexpenses"] else 1
        data["id"] = expenseId
        doc[expenseType + "expenses"].append(data)
        doc["eventype"] = expenseType + "expenseinsertion"

    elif last is None and data is None:
        doc = {"userid": userid, "fixexpenses": [], "varexpenses": []}
        doc["eventype"] = "usercreation"
    
    
    doc["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return doc