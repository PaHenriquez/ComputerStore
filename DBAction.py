import mariadb

def AttemptLogin(Email, password):
    query = "select * from Spoiled_Users where Email = \"{}\" and Password = \"{}\" limit 1".format(Email, password)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindUser(userID):
    connect = mariadb.connect(user='root', password='MyDatabase',host='localhost', database='SpoiledEgg')
    cur = connect.cursor()
    query = "select * from Spoiled_Users where ID = \"{}\"limit 1".format(userID)
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindAddressAndStoreCredit(userID):
    query = "select * from Spoiled_Customer where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindPayment(userID): 
    cnxS = mariadb.connect(user='root', password='MyDatabase',host='localhost', database='SpoiledEgg')
    curS = cnxS.cursor(buffered=True)
    query = "select * from Spoiled_Payment where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    print(result)
    if len(result) == 1:
        return result[0]
    else:
        return False

def InsertPost(userID, subForum, title, content, Author):
    query1 = "SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = \'Forum\' AND   TABLE_NAME  = \"All_post\""
    curF.execute(query1)
    Post_ID = curF.fetchone()[0]
    query2 = "insert into All_post (Post_ID, Which_subforum, Author) VALUES({}, \"{}\", \"{}\" )".format(Post_ID, subForum, Author)
    curF.execute(query2)
    cnxF.commit()
    query3 = "insert into Post_{} (Post_ID, Post_title, Author) VALUES({}, \"{}\", \"{}\")".format(subForum, Post_ID, title, Author)
    curF.execute(query3)
    cnxF.commit()
    query4 = "insert into Comment_{} (Comment_content, Post_ID, Author) VALUES(\"{}\", {}, \"{}\")".format(subForum, content, Post_ID, Author)
    curF.execute(query4)
    cnxF.commit()

def GetPosts(subForum, startIndex, endIndex): #this is for the forum loading
    query= "select * from Post_{} ORDER BY PostDate DESC limit {}, {}".format(subForum, startIndex, endIndex)
    curF.execute(query)
    return curF.fetchall()

def GetPostByID(subForum, Post_ID):
    query = "SELECT * FROM Post_{} WHERE Post_ID = {}".format(subForum, Post_ID)
    curF.execute(query)
    return curF.fetchall()

def GetCommentByPostID(subForum, Post_ID):
    query = "SELECT * FROM Comment_{} WHERE Post_ID = {} ORDER BY PostDate DESC".format(subForum, Post_ID)
    curF.execute(query)
    return curF.fetchall()

def GetRepliesByCommentID(subForum, Comment_ID):
    query = "SELECT * FROM Reply_{} WHERE Comment_ID = {} ORDER BY PostDate DESC".format(subForum, Comment_ID)
    curF.execute(query)
    return curF.fetchall()

def GetCommentByCommentID(subForum, Comment_ID):
    query = "SELECT * FROM Comment_{} WHERE Comment_ID = {}".format(subForum, Comment_ID)
    curF.execute(query)
    return curF.fetchall()

def InsertReplyByCommentID(subForum, Commend_ID, content, Author):
    query = "insert into Reply_{} (Reply_content, Comment_ID, Author) VALUES(\"{}\", {}, \"{}\")".format(subForum, content, Commend_ID, Author)
    curF.execute(query)
    cnxF.commit()

def InsertCommentByPostID(subForum, Post_ID, content, Author):
    query = "insert into Comment_{} (Comment_content, Post_ID, Author) VALUES(\"{}\", {}, \"{}\")".format(subForum, content, Post_ID, Author)
    curF.execute(query)
    cnxF.commit()

#----------------------------------------------------------------------------------------------------
def Insert_New_Payment(UserID, Payment_card=0, Name_On_Card="N/A", Billing_Address="N/A"):
    cur.execute("INSERT INTO Spoiled_Payment(ID,Payment_Card,Name_On_Card,Billing_Address)" +
                "VALUES(?,?,?,?);", (UserID, Payment_card, Name_On_Card, Billing_Address))
    cnx.commit()

def DoesUsernameExist(username):
    query = "select Username from Spoiled_Users where Username = \"{}\"".format(username)
    cur.execute(query)
    result = cur.fetchone()
    if(result != None):
        return True
    else:
        return False

def DoesEmailExist(email):
    query = "select Email from Spoiled_Users where Email = \"{}\"".format(email)
    cur.execute(query)
    result = cur.fetchone()
    if(result != None):
        return True
    else:
        return False

def Insert_New_User(ID,Username,Email,Password,Phone_Number,User_Type,Type = "n/a",Company_Name = "n/a"): 
    #cnx= Connect_to_Mariadb()
    #cur = cnx.cursor()
    cur.execute("INSERT INTO Spoiled_Users(ID,Username,Email,Password,Phone_Number,User_Type) \
              VALUES(?,?,?,?,?,?);",(ID, Username, Email, Password, Phone_Number, User_Type))
    if User_Type == "Customer":          
        cur.execute(
            "INSERT INTO Spoiled_Customer(ID,Store_Credit)" + 
            "VALUES(?,?);",(ID,0))    
    elif User_Type == "Business_Partner":
        cur.execute(
            "INSERT INTO Spoiled_Business_Partner(ID,Company_Name,Partner_Type)" + 
            "VALUES(?,?,?);",(ID,Company_Name,Type))
    elif User_Type == "Employee":
        cur.execute(
            "INSERT INTO Spoiled_Employee(ID,Employee_Type)" + 
            "VALUES(?,?);",(ID,Type))    
    cnx.commit()

def Update_Data(Table,Attribute,New_Value,ID):
    cur.execute(
        "UPDATE Spoiled_" + Table + " SET " + Attribute + " = \"{}\" WHERE ID = \"{}\"".format(New_Value,ID))
    cnx.commit()

def GetProduct(typeOfProduct, startIndex, endIndex): #this is for the forum loading
    query= "select * from Spoiled_{} ORDER BY Name DESC limit {}, {}".format(typeOfProduct, startIndex, endIndex)
    curS.execute(query)
    return curS.fetchall()

def InsertBid(Item_ID, Company, CompanyType, bid):
    query = "insert into Spoiled_Bids (Item_ID, Company_Name, Bid, Company_Type) VALUES({}, \"{}\", {}, \"{}\")".format(Item_ID, Company, bid, CompanyType)
    curS.execute(query)
    cnxS.commit()
    
def FindCompany(userID):
    query = "select * from Spoiled_Business_Partner where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False  

def GetBids(item_ID, startIndex, endIndex, typeOfBid):
    query= "select * from Spoiled_Bids where (Item_ID = {} AND Company_Type = \"{}\") ORDER BY Bid DESC limit {}, {}".format(item_ID, typeOfBid, startIndex, endIndex)
    curS.execute(query)
    return curS.fetchall()

def FindEmployee(userID):
    query = "select * from Spoiled_Employee where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False        

def AcceptBid(Item_ID, userID, typeOfBid):
    if typeOfBid == "Shipper":
        query1 = "UPDATE Spoiled_Item SET Shipper_ID={} WHERE Item_ID={}".format(userID, Item_ID)
        curS.execute(query1)
        cnxS.commit()
    else:
        query1 = "UPDATE Spoiled_Item SET Supplier_ID={} WHERE Item_ID={}".format(userID, Item_ID)
        curS.execute(query1)
        cnxS.commit()
    query2 = "DELETE FROM Spoiled_Bids WHERE (Item_ID={} and Company_Type=\"{}\")".format(Item_ID, typeOfBid)
    curS.execute(query2)
    cnxS.commit()

def FindBidder(CompanyName):
    query= "select * from Spoiled_Business_Partner where Company_Name = \"{}\" limit 1".format(CompanyName)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def getTaboo(startIndex, endIndex):
    query = "select * from Taboo limit {}, {}".format(startIndex, endIndex)
    curF.execute(query)
    result = curF.fetchall()
    if len(result) > 0:
        return list(set().union(*result))
    else:
        return False

def GetAppeals(startIndex, endIndex): #this is for the forum loading
    query= "select * from Spoiled_Users where AppealText IS NOT NULL ORDER BY AppealDate DESC limit {}, {}".format(startIndex, endIndex)
    curS.execute(query)
    return curS.fetchall()

def CreateAppeal(userID, content):
    query = "UPDATE Spoiled_Users SET AppealText = \"{}\", Appealed = 1, AppealDate = current_timestamp() where ID = {}".format(content, userID)
    curS.execute(query)
    cnxS.commit()

def DecideAppeal(userID, decision, canAppealAgain):
    if decision:
        query1 = "UPDATE Spoiled_Users SET Warnings = 0, AppealText = NULL where ID = {}".format(userID)
    else:
        query1 = "UPDATE Spoiled_Users SET AppealText = NULL where ID = {}".format(userID)
    curS.execute(query1)
    cnxS.commit()
    if canAppealAgain:
        query2 = "UPDATE Spoiled_Users SET Appealed = 0 where ID = {}".format(userID)
    else:
        query2 = "UPDATE Spoiled_Users SET Appealed = 1 where ID = {}".format(userID)
    curS.execute(query2)
    cnxS.commit()

def GetWarning(userID):
    query = "select Warnings from Spoiled_Users where ID = {}".format(userID)
    curS.execute(query)
    result = curS.fetchall()
    if len(result) == 1:
        return result[0][0]
    else:
        return False

def AddWarning(userID):
    query = "UPDATE Spoiled_Users SET Warnings = {} where ID = {}".format(GetWarning(userID) + 1, userID)
    curS.execute(query)
    cnxS.commit()


cnx = mariadb.connect(user='root', password='MyDatabase',host='localhost', database='SpoiledEgg')
cur = cnx.cursor()
cnxS = mariadb.connect(user='root', password='MyDatabase',host='localhost', database='SpoiledEgg')
curS = cnxS.cursor(buffered=True)
cnxF = mariadb.connect(user='root', password='MyDatabase',host='localhost', database='Forum')
curF = cnxF.cursor(buffered=True)


# curS.execute("INSERT INTO AVOID(Email) VALUES(\"somegmail@gmail.com\");")
# print(curS.execute("select * from AVOID"))
# 6 RegCut, #4 business: retailer - #5 business: shipper, #2 Employee - #1 Manager
# Insert_New_User(cur,6413001,"Snortz","Cheese@aol.com","CornChips","101-100-1000","Customer") 
# Insert_New_User(cur,5045100,"ShipGuy","DefXe@aol.com","Shippie","099-999-1111","Business_Partner","Shipper","FedEx")
# Insert_New_User(cur,123456,"Publius","publius@gmail.com","pass","911","Employee", "Manager")


# Insert_New_Item(cur,1000001,"Monitor",4045100,500,1000,0,"")
# Insert_New_Item(cur,2000001,"GPU",4045100,500,5000,0,"rtx3080 FE")
# Insert_New_Item(cur,2000002,"GPU",4045100,500,7000,0,"rtx3080 FE CP Edition")


