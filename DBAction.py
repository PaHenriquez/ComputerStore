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
    query = "select * from Spoiled_Users where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
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
    query = "select * from Spoiled_Payment where ID = \"{}\"limit 1".format(userID)
    curS.execute(query)
    result = curS.fetchall()
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




cnxS = mariadb.connect(user='root', password='password',host='localhost', database='SpoiledEgg')
curS = cnxS.cursor(buffered=True)
cnxF = mariadb.connect(user='root', password='password',host='localhost', database='Forum')
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


