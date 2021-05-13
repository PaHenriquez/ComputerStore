#https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
import mariadb

##Convert ui file to python script
##python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py

def Connect_to_Mariadb():
    connection = mariadb.connect(
    user = "root",
    password = "MyDatabase",
    host = "localhost",
    port = 3306,
    database = "SpoiledEgg")
       
    return connection
    
def SelectItem(cur,Filter = "ALL"):
    if Filter == "ALL":
        cur.execute(
            "SELECT * FROM Spoiled_Item;"
        )
        
def SelectUser(cur, Filter = "All"):
    if Filter == "All":
        cur.execute(
            "SELECT * FROM Spoiled_Users;"
        )

def SelectONEUser(cur,ID,Filter = "All"):
    if Filter == "All":
        cur.execute(
            "SELECT * FROM Spoiled_Users WHERE ID = ?;",(ID)
        )        
       
def Update_Data(cur,Table,Attribute,New_Value,ID):
    cur.execute(
        "UPDATE Spoiled_" + Table + " SET " + Attribute + " = " + New_Value + " WHERE ID = ?;",(ID))

def Insert_New_User(cur,ID,Username,Email,Password,Phone_Number,User_Type,Type = "n/a",Company_Name = "n/a"): 
    cur.execute(
        "INSERT INTO Spoiled_Users(ID,Username,Email,Password,Phone_Number,User_Type) \
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

def Insert_New_Item(cur,Item_ID,Name,Type_of_Part,Shipper_ID,Description,Quantity,Price,Rating):
    cur.execute(
        "INSERT INTO Spoiled_Item(Item_ID,Name,Type_of_Part,Shipper_ID,Description,Quantity,Price,Rating)\
         VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(Item_ID,Name,Type_of_Part,Shipper_ID,Description,Quantity,Price,Rating))
    cur.execute(
        "INSERT INTO Spoiled_" + Type_of_Part + "(Item_ID,Name)\
         VALUES(?,?);",(Item_ID,Name))   

#Functions each item dialog                 
def Current_Monitors():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'Monitor'")
    return cur    
def Current_CPU(): 
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'CPU'")
    return cur    
def Current_GPU(): 
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'GPU'") 
    return cur    
def Current_PSU():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'PSU'")
    return cur
def Current_PC_Cases():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'PC_Cases'")
    return cur
def Current_Storage():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'Storage'")
    return cur
def Current_Memory():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'Memory'")
    return cur
def Current_Motherboard():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'Motherboard'")
    return cur
def Current_Software():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'Software'")
    return cur
def Current_Prebuilds():
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'Prebuilds'")
    return cur
def Current_Laptops(): 
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Type_of_Part = 'Laptops'")
    return cur

def Current_Cart(ID):
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Cart WHERE ID = ?;",(ID,))
    return cur
def GetItemInfo(Item_ID):
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT * FROM Spoiled_Item WHERE Item_ID = ?;",(Item_ID,))
    temp = cur.fetchone()
    return temp

def GetPaymentInfo(ID):
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT Payment_Card FROM Spoiled_Payment WHERE ID = ?",(ID,))
    Payment = cur.fetchone()
    cur.execute("SELECT Store_Credit FROM Spoiled_Customer WHERE ID = ?",(ID,))
    Cred = cur.fetchone()
    result = ["",0]
    if Payment:
        result[0] = Payment   
    if Cred:
        result[1] = Cred
    return result
    
def FindShipper(ID):
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("SELECT Shipper_ID FROM Spoiled_Item WHERE Item_ID = ?",(ID,))
    Shipper = cur.fetchone()
    connection.close()
    return Shipper
    
def GetShipper(ID):
    shippers = []
    cur = Current_Cart(ID)
    for item in cur:
        shippers.append(FindShipper(item[1])[0])
    return most_common_oneliner(shippers)    

def GetUsername(ID):
    print(ID)
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute(
            "SELECT * FROM Spoiled_Users WHERE ID = ?;",(ID,)
        ) 
    Name = cur.fetchone()
    print(Name)
    connection.close()
    return Name[1]    
    
def most_common_oneliner(lst):
  return max(set(lst), key=lst.count)        
 
def Delete_Cart(ID):
    connection = Connect_to_Mariadb()
    cur = connection.cursor()
    cur.execute("DELETE FROM Spoiled_Cart WHERE ID  = ?",(ID,))
    connection.commit()
    connection.close()
 
def StartUp():

        connection = Connect_to_Mariadb()
        cur = connection.cursor()
  
        #5 RegCut, #3 business: retailer - #4 business: shipper, #1 Employee - #0 Manager
        Insert_New_User(cur,6413001,"Snortz","Cheese@aol.com","CornChips","101-100-1000","Customer") 
        Insert_New_User(cur,1000001,"Blorg","Blorg@aol.com","ManagerMan","999-898-0999","Employee","Manager")
        Insert_New_User(cur,5045100,"ShipGuy","DefXe@aol.com","Shippie","099-999-1111","Business_Partner","Shipper","FedEx")
        Insert_New_User(cur,4045100,"Target","UPS@aol.com","H","111-111-1111","Business_Partner","Retailer","Target")

        Insert_New_Item(cur,1000001,"Razor_Blade","Monitor",5045100,"Best monitor for gaming\nDETAILS",500,1000,0)
        Insert_New_Item(cur,1000002,"Potato_Sac","Monitor",5045100,"Best monitor for gaming\nDETAILS",750,2000,0)
        Insert_New_Item(cur,1000003,"Trash","Monitor",5045100,"DO NOT BUY THIS JUNK\n",5000,10,0)
        
        Insert_New_Item(cur,2000001,"Rtx3080 FE CP Edition","GPU",5045100,"YOU CAN SEE IT BUT CANT HAVE IT\n",1,17000,0)
        Insert_New_Item(cur,2000002,"Rtx3080 FE","GPU",5045100,"PLEASE BUY THIS\n\n",3,15000,0)
        Insert_New_Item(cur,2000003,"Rtx3070 FE","GPU",5045100,"PLEASE BUY THIS\n\n",30,5000,0)
        Insert_New_Item(cur,2000004,"Rtx3090 FE","GPU",5045100,"YOU CAN SEE IT BUT CANT HAVE IT\n",1,17000,0)
        
        Insert_New_Item(cur,3000001,"Ryzen 5900x","CPU",5045100,"Best CPU for gaming\nDETAILS",2,1000,0)
        Insert_New_Item(cur,3000002,"Intel I7","CPU",5045100,"An okay CPU\nDETAILS",750,500,0)
        
        
        Insert_New_Item(cur,4000001,"MSI x570 Pro","Motherboard",5045100,"Best Motherboard for gaming\nDETAILS",200,100,0)
        Insert_New_Item(cur,4000002,"Aorus","Motherboard",5045100,"You need to buy",200,100,0)
        
        Insert_New_Item(cur,5000001,"Pink PC_Case","PC_Cases",5045100,"For those who love pink\nDETAILS",250,150,0)
        Insert_New_Item(cur,5000002,"White PC_Case","PC_Cases",5045100,"For those who love white",300,90,0)
        Insert_New_Item(cur,5000003,"Clear Case","PC_Cases",5045100,"For those who love clear",300,90,0)
        
        Insert_New_Item(cur,6000001,"Corsair RM750x","PSU",5045100,"Great Deal\nDETAILS",2500,150,0)
        Insert_New_Item(cur,6000002,"Evga 1000-T2","PSU",5045100,"Amazing Deal",300,190,0)
        Insert_New_Item(cur,6000003,"Corsair SF750","PSU",5045100,"Its alright",200,290,0)
        
        Insert_New_Item(cur,7000001,"TridentZ RGB","Memory",5045100,"I have 2 of these sticks\nDETAILS",400,300,0)
        Insert_New_Item(cur,7000002,"Ratchet RAM","Memory",5045100,"This is Ratchet",3000,90,0)
        
        Insert_New_Item(cur,8000001,"Samsung Inland 980 PRO","Storage",5045100,"We only sell ssd\nDETAILS",550,200,0)
        Insert_New_Item(cur,8000002,"Western Blue","Storage",5045100,"Cheap ole storage",300,90,0)
        
        Insert_New_Item(cur,9000001,"FakeMac","Laptops",5045100,"For those who cant afford mac\nDETAILS",550,2000,0)
        Insert_New_Item(cur,9000002,"Cheap_Dell","Laptops",5045100,"Cheap Dell laptop",3000,390,0)
        
        Insert_New_Item(cur,9000003,"Beginner_Prebuild","Prebuilds",5045100,"Prebuilds SUCK\nDETAILS",500,1200,0)
        Insert_New_Item(cur,9000004,"Advanced_Prebuild","Prebuilds",5045100,"For the beginner gamer",300,9000,0)
        
        Insert_New_Item(cur,9000013,"IOS","Software",5045100,"For MAC USERS",500,200,0)
        Insert_New_Item(cur,9000014,"LINUX","Software",5045100,"For the coders of the world",300,90,0)
        Insert_New_Item(cur,9000015,"Windows","Software",5045100,"For the Oldies of the world",3000,90,0)
 
        connection.commit()
        
        return connection.cursor() 


#StartUp()