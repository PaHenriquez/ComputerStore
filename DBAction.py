import mysql.connector as maria

def AttemptLogin(curS, Email, password):
    query = "select * from All_user where Email = \"{}\" and Password = \"{}\" limit 1".format(Email, password)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindUser(curS, userID):
    query = "select * from All_user where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindAddressAndStoreCredit(curS, userID):
    query = "select * from Customer where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindPayment(curS, userID):
    query = "select * from Payment where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

        