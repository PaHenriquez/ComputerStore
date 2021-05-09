import mariadb

def AttemptLogin(Email, password):
    query = "select * from Spoiled_Users where Email = \"{}\" and Password = \"{}\" limit 1".format(Email, password)
    cur.execute(query)
    result = cur.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindUser(userID):
    query = "select * from Spoiled_Users where ID = \"{}\"limit 1".format(userID)
    cur.execute(query)
    result = cur.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindAddressAndStoreCredit(userID):
    query = "select * from Spoiled_Customer where ID = \"{}\"limit 1".format(userID)
    cur.execute(query)
    result = cur.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

def FindPayment(userID):
    query = "select * from Spoiled_Payment where ID = \"{}\"limit 1".format(userID)
    cur.execute(query)
    result = cur.fetchall()
    if len(result) == 1:
        return result[0]
    else:
        return False

# ---------------------------------------------------------------------
def SelectItem(cur, Filter = "ALL"):
    if Filter == "ALL":
        cur.execute(
            "SELECT * FROM Spoiled_Item;"
        )
        
def SelectUser(cur, userID, Filter = "All"):
    if Filter == "All":
        cur.execute(
            "SELECT * FROM Spoiled_Users where ID = ?;", (userID)
            )
       
def Update_Data(Table,Attribute,New_Value,ID):
    cur.execute(
        "UPDATE Spoiled_" + Table + " SET " + Attribute + " = \"{}\" WHERE ID = \"{}\"".format(New_Value,ID))
    cnx.commit()

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
   

def Insert_New_Item(cur,Item_ID,Type_of_Part,Shipper_ID,Quantity,Price,Rating,Name):
    cur.execute(
        "INSERT INTO Spoiled_Item(Item_ID,Type_of_Part,Shipper_ID,Quantity,Price,Rating)\
         VALUES(?, ?, ?, ?, ?, ?);",(Item_ID,Type_of_Part,Shipper_ID,Quantity,Price,Rating))
    cur.execute(
        "INSERT INTO Spoiled_" + Type_of_Part + "(Item_ID,Name)\
         VALUES(?,?);",(Item_ID,Name))   
               
#REMEMBER INSERT for each items specs 

def Filter(cur,price = 0,pC = ">=",rating = 0,rC = ">=",Type = "All",rAD = "ASC",pAD = "ASC",Table = "Spoiled_Item"):
    cur.execute("SELECT * FROM " + Table + " WHERE Price " + pC + " " + str(price) + "AND" +
                                                   "Rating " + rC + " " + str(price) + "AND" +
                                                   "Type_of_Part = " + Type + " ORDER BY " +
                                                   "Rating" + rAD + ",Price " + pAD +";")

def Filter_by_Monitor(cur,RRvalue = 0,Dvalue = 0,Rvalue = "All"):
    if Rvalue == "All":
        cur.execute("CREATE OR REPLACE VIEW Monitor_list AS " +
                    "SELECT * FROM Spoiled_Monitor WHERE Refresh_Rate >= " + str(RRvalue) + " AND " +
                                                        "Dimensions >= " + str(Dvalue) + ";")
    else:
        cur.execute("CREATE OR REPLACE VIEW Monitor_list AS " +
                    "SELECT * FROM Spoiled_Monitor WHERE Refresh_Rate >= " + str(RRvalue) + " AND " +
                                                        "Dimensions >= " + str(Dvalue) + " AND " +
                                                        "Resolution = Rvalue;")

def Filter_by_GPU(cur,Architecture):
    cur.execute("CREATE OR REPLACE VIEW GPU_list AS " +
                "SELECT * FROM Spoiled_GPU WHERE Architecture = ?;",(Architecture))
    
def Filter_by_CPU(cur,Architecture):
    cur.execute("CREATE OR REPLACE VIEW CPU_list AS " +
                "SELECT * FROM Spoiled_CPU WHERE Architecture = ?;",(Architecture))    
                
def Filter_by_Cases(cur,Material):
    cur.execute("CREATE OR REPLACE VIEW PC_Case_list AS " +
                "SELECT * FROM Spoiled_PC_Cases WHERE Material = ?;",(Material))     

def Filter_by_Motherboard(cur,ArchitectureC):
    cur.execute("CREATE OR REPLACE VIEW MB_list AS " +
                "SELECT * FROM Spoiled_Motherboard WHERE Architecture_Compatibility = ?;",(ArchitectureC)) 
                
def Filter_by_PSU(cur,Wattage):
    cur.execute("CREATE OR REPLACE VIEW PSU_list AS " +
                "SELECT * FROM Spoiled_PSU WHERE Wattage >= ?;",(Wattage))     

def Filter_by_Memory(cur,Total_Memory = 0,Speed = 0):
    cur.execute("CREATE OR REPLACE VIEW Memory_list AS " +
                "SELECT * FROM Spoiled_Memory WHERE Total_Memory >= ? AND Speed >= ?;",(Total_Memory,Speed)) 

def Filter_by_Storage(cur,Total_Memory = 0 ,Type_Of_Storage = 0):
    cur.execute("CREATE OR REPLACE VIEW Storage_list AS " +
                "SELECT * FROM Spoiled_Storage WHERE Total_Memory >= ? AND Type_Of_Storage = ?;",(Total_Memory,Type_Of_Storage))
 
def Filter_by_LoP(cur,Memory = 0,Storage = 0,GPU = "Empty",CPU = "Empty",PSU = 0,LoP = 0): #LoP = 0,1,2
    if LoP == 0: # ALL
        if GPU == "Empty" and CPU == "Empty":
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Memory >= ? AND Storage >= ? AND PSU >= ?;",(Memory,Storage,PSU))
        elif GPU != "Empty":                
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Memory >= ? AND Storage >= ? AND PSU >= ? AND GPU = ?;",(Memory,Storage,PSU,GPU))
        elif CPU != "Empty":                
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Memory >= ? AND Storage >= ? AND PSU >= ? AND CPU = ?;",(Memory,Storage,PSU,CPU)) 
        else:
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Memory >= ? AND Storage >= ? AND PSU >= ? AND CPU = ? AND GPU = ?;",(Memory,Storage,PSU,CPU,GPU))
    elif LoP == 1: # Laptop
        if GPU == "Empty" and CPU == "Empty":
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 1, Memory >= ? AND Storage >= ? AND PSU >= ?;",(Memory,Storage,PSU))
        elif GPU != "Empty":                
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 1, Memory >= ? AND Storage >= ? AND PSU >= ? AND GPU = ?;",(Memory,Storage,PSU,GPU))
        elif CPU != "Empty":                
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 1, Memory >= ? AND Storage >= ? AND PSU >= ? AND CPU = ?;",(Memory,Storage,PSU,CPU)) 
        else:
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 1, Memory >= ? AND Storage >= ? AND PSU >= ? AND CPU = ? AND GPU = ?;",(Memory,Storage,PSU,CPU,GPU))                                    
    
    elif LoP == 2: # Laptop
        if GPU == "Empty" and CPU == "Empty":
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 2, Memory >= ? AND Storage >= ? AND PSU >= ?;",(Memory,Storage,PSU))
        elif GPU != "Empty":                
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 2, Memory >= ? AND Storage >= ? AND PSU >= ? AND GPU = ?;",(Memory,Storage,PSU,GPU))
        elif CPU != "Empty":                
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 2, Memory >= ? AND Storage >= ? AND PSU >= ? AND CPU = ?;",(Memory,Storage,PSU,CPU)) 
        else:
            cur.execute("CREATE OR REPLACE VIEW Laptop_list AS " +
                        "SELECT * FROM Spoiled_Laptops_and_PreBuilds WHERE Laptop_or_Prebuild = 2, Memory >= ? AND Storage >= ? AND PSU >= ? AND CPU = ? AND GPU = ?;",(Memory,Storage,PSU,CPU,GPU))    
      
def Filter_by_Software(OS_choice,cur):
    cur.execute("CREATE OR REPLACE VIEW Software_list AS " +
                "SELECT * FROM Spoiled_Software WHERE OS_choice = ?;",(OS_choice))  

def Connect_to_Mariadb():
    connection = mariadb.connect(
    user = "root",
    password = "1234",
    host = "localhost",
    port = 3306,
    database = "SpoiledEgg")
    return connection


# testing insert payment functionality - Raystorm

def Insert_New_Payment(UserID,Payment_card = 0,Name_On_Card ="N/A",Billing_Address="N/A"):
    cur.execute("INSERT INTO Spoiled_Payment(ID,Payment_Card,Name_On_Card,Billing_Address)"+
        "VALUES(?,?,?,?);",(UserID,Payment_card,Name_On_Card,Billing_Address))
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
    
    

# cnxS = maria.connect(user='root', password='password',host='localhost', database='SpoiledEgg')
# curS = cnxS.cursor(buffered=True)
# curS.execute("INSERT INTO Spoiled_Users(ID,Username,Email,Password,Phone_Number,User_Type) VALUES(123456,\"Publius\",\"publius@gmail.com\",\"pass\",\"911\",\"Employee\");")

cnx = Connect_to_Mariadb()
cur = cnx.cursor()

#print(cur.execute("Select * From Spoiled_Users where Phone_Number = 999"))

# curS.execute("INSERT INTO AVOID(Email) VALUES(\"somegmail@gmail.com\");")
# print(curS.execute("select * from AVOID"))
# 6 RegCut, #4 business: retailer - #5 business: shipper, #2 Employee - #1 Manager
# Insert_New_User(cur,6413001,"Snortz","Cheese@aol.com","CornChips","101-100-1000","Customer") 
# Insert_New_User(cur,5045100,"ShipGuy","DefXe@aol.com","Shippie","099-999-1111","Business_Partner","Shipper","FedEx")
# Insert_New_User(cur,123456,"Publius","publius@gmail.com","pass","911","Employee", "Manager")


# Insert_New_Item(cur,1000001,"Monitor",4045100,500,1000,0,"")
# Insert_New_Item(cur,2000001,"GPU",4045100,500,5000,0,"rtx3080 FE")
# Insert_New_Item(cur,2000002,"GPU",4045100,500,7000,0,"rtx3080 FE CP Edition")



#-------------------Raystorm testing------------------------------

#Insert_New_User(cur, 1, "Snortz", "Cheese@aol.com","test", "101-100-1000", "Customer")
#Insert_New_Payment(cur,1,"23")
#Insert_New_Payment(cur, 1, "00010899", "Snortz", "Nyc")
#test = FindPayment(cur,1)
#print(test)
#Update_Data(cur,'Payment','Name_On_Card','ray',1)
#Update_Data(cur,'Users','Phone_Number','9',1)
#test = FindPayment(cur,1)
#print(test)

#test = DoesUsernameExist(cur,"snortz")
#print(test)




