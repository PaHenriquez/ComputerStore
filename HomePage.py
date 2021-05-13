import sys

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QLabel, QFormLayout, QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QPixmap, QFont
from PyQt5 import QtCore
from Page_Logic import *
from Forum import *
from DBAction import *
from random import randint

from Page_Logic import *
from LoginScreen import *
from AccountDetail import *
from BiddingPage import BiddingWindow
from ViewAppeal import ViewAppealWindow


class HomePage(QMainWindow):

    def __init__(self,user = 0):
        self.user = user
        super(HomePage,self).__init__()
        uic.loadUi("UIs/HomePgae.ui",self)
        #Featured_Images
        self.NameImage1 = self.Manage_Image1()
        self.NameImage2 = self.Manage_Image2()
        self.NameImage3 = self.Manage_Image3()
        self.NameImage4 = self.Manage_Image4()
        self.NameImage5 = self.Manage_Image5()
        self.NameImage6 = self.Manage_Image6()
        
        #MAIN BUTTONS
        if user != 0:
            self.Loggout_Button.setText("Loggout")
            self.Loggout_Button.clicked.connect(lambda: self.clickedLoginNOutBtn(user)) 
            self.Account_Button.clicked.connect(lambda: self.clickedAccount(user))
            self.Cart_Button.clicked.connect(self.load_Cart)
            #Add to carts Items
            self.Add_to_Cart1.clicked.connect(lambda: self.addToCart(self.NameImage1,user))
            self.Add_to_Cart2.clicked.connect(lambda: self.addToCart(self.NameImage2,user))
            self.Add_to_Cart3.clicked.connect(lambda: self.addToCart(self.NameImage3,user))
            self.Add_to_Cart4.clicked.connect(lambda: self.addToCart(self.NameImage4,user))
            self.Add_to_Cart5.clicked.connect(lambda: self.addToCart(self.NameImage5,user))
            self.Add_to_Cart6.clicked.connect(lambda: self.addToCart(self.NameImage6,user))
            
            prefix = int(str(user)[0])
            self.Bidding_Button.setEnabled(False)
            self.Appeals_Button.hide()
            if prefix in [1,2,4,5]:
                self.Bidding_Button.setEnabled(True)
                BiddingUI = BiddingWindow(SpoiledEGG,0,self.user,"GPU")
                self.Bidding_Button.clicked.connect(lambda: self.GoToWindow(BiddingUI))
                BiddingUI.HomePageBtn.clicked.connect(lambda: self.GoToWindow(HomePage(self.user)))
                if prefix == 1:
                    self.Appeals_Button.show()
                    self.Appeals_Button.clicked.connect(lambda: self.GoToWindow(ViewAppealWindow(0,SpoiledEGG,HomePage(self.user))))
        else:  
            self.Bidding_Button.setEnabled(False)
            self.Account_Button.setEnabled(False)
            self.Appeals_Button.hide()
            self.Loggout_Button.clicked.connect(lambda: self.clickedLoginNOutBtn(user))
            self.Cart_Button.setEnabled(False)
            self.Add_to_Cart1.setEnabled(False)
            self.Add_to_Cart2.setEnabled(False)
            self.Add_to_Cart3.setEnabled(False)
            self.Add_to_Cart4.setEnabled(False)
            self.Add_to_Cart5.setEnabled(False)
            self.Add_to_Cart6.setEnabled(False)     

        self.Forums_Button.clicked.connect(self.load_Forum)

        #Items button
        self.Monitors_Button.clicked.connect(self.load_Monitors)
        self.CPU_Button.clicked.connect(self.load_CPU)
        self.GPU_Button.clicked.connect(self.load_GPU)
        self.PSU_Button.clicked.connect(self.load_PSU)
        self.Storage_Button.clicked.connect(self.load_Storage)
        self.Memory_Button.clicked.connect(self.load_Memory)
        self.Motherboard_Button.clicked.connect(self.load_Motherboard)
        self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
        self.Software_Button.clicked.connect(self.load_Software)
        self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
        self.Laptops_Button.clicked.connect(self.load_Laptops)
        
       
        
    def addToCart(self,Item_ID,ID):
        cur = GetItemInfo(Item_ID[0:7])
        Name = cur[1]
        Price = cur[6]
        connection = Connect_to_Mariadb()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Spoiled_Cart WHERE ID = ? AND Item_ID = ?",(ID,Item_ID))
        item = cursor.fetchone()
        if item is None:
            cursor.execute("INSERT INTO Spoiled_Cart(ID,Item_ID,Name,Price,Occurence) VALUES(?,?,?,?,?)",(ID,int(Item_ID[0:7]),Name,Price,1))
            connection.commit()
        else:
            cursor.execute("UPDATE Spoiled_Cart SET Occurence = ? WHERE ID = ? AND Item_ID = ?;",(item[4]+1,ID,Item_ID))
            connection.commit()
        cursor.close()
        
        self.GoToWindow(ItemAddedPage(self.user,HomePage(self.user)))         
    
    def load_Monitors(self):
        self.GoToWindow(ItemsPage(self.user,"Monitors"))   
        
    def load_CPU(self):
        self.GoToWindow(ItemsPage(self.user,"CPU"))
        
    def load_GPU(self):
        self.GoToWindow(ItemsPage(self.user,"GPU"))
            
    def load_PSU(self):
        self.GoToWindow(ItemsPage(self.user,"PSU"))
        
    def load_Storage(self):
        self.GoToWindow(ItemsPage(self.user,"Storage"))

    def load_Memory(self):
        self.GoToWindow(ItemsPage(self.user,"Memory"))
        
    def load_Motherboard(self):
        self.GoToWindow(ItemsPage(self.user,"Motherboard")) 
        
    def load_PC_Cases(self):
        self.GoToWindow(ItemsPage(self.user,"PC_Cases"))
        
    def load_Software(self):
        self.GoToWindow(ItemsPage(self.user,"Software"))
            
    def load_Prebuilds(self):
        self.GoToWindow(ItemsPage(self.user,"Prebuilds"))    

    def load_Laptops(self):
        self.GoToWindow(ItemsPage(self.user,"Laptops"))    
        
    def load_Cart(self):
        Cart = CartPage(self.user)
        self.GoToWindow(Cart)
           
    def load_Forum(self):
        FrontPageUI = HomePage(self.user)
        ForumUI = ForumWindow(1, "GPU", self.user, SpoiledEGG, FrontPageUI)
        self.GoToWindow(ForumUI)
    
    def clickedLoginNOutBtn(self, userID): ## COMPLETE
        #if someone clicks login botton with a valid userID, then that
        #means they want to log out, so when userID is not 0, we call frontpage(0),
        if userID != False:
            self.GoToWindow(HomePage())
        else:
            self.GoToWindow(LoginScreenWindow(SpoiledEGG,HomePage))
    
    def clickedAccount(self, userID):
        AccountDetailUI = AccountDetail(userID,SpoiledEGG,HomePage(userID))
        self.GoToWindow(AccountDetailUI)
        
    def GoToWindow(self, window):
        SpoiledEGG.removeWidget(SpoiledEGG.currentWidget())
        SpoiledEGG.addWidget(window)
        SpoiledEGG.setCurrentIndex(0)
 
    #Load featured images    
    def Manage_Image1(self,Name = "6000003.jpg"):
        self.label = QLabel(self)
        self.label.resize(181,181)
        self.pm = QPixmap(Name)
        self.label.setPixmap(self.pm)
        self.label.move(230,220)
        self.label.show()
        return Name[0:7]    
    def Manage_Image2(self,Name = "5000003.jpg"):
        self.label = QLabel(self)
        self.label.resize(181,181)
        self.pm = QPixmap(Name)
        self.label.setPixmap(self.pm)
        self.label.move(460,220)
        self.label.show() 
        return Name[0:7]
    def Manage_Image3(self,Name = "7000002.jpg"):
        self.label = QLabel(self)
        self.label.resize(181,181)
        self.pm = QPixmap(Name)
        self.label.setPixmap(self.pm)
        self.label.move(670,220)
        self.label.show() 
        return Name[0:7]
    def Manage_Image4(self,Name = "2000001.jpg"):
        self.label = QLabel(self)
        self.label.resize(181,181)
        self.pm = QPixmap(Name)
        self.label.setPixmap(self.pm)
        self.label.move(230,450)
        self.label.show() 
        return Name[0:7]
    def Manage_Image5(self,Name = "3000001.jpg"):
        self.label = QLabel(self)
        self.label.resize(181,181)
        self.pm = QPixmap(Name)
        self.label.setPixmap(self.pm)
        self.label.move(460,450)
        self.label.show() 
        return Name[0:7]
    def Manage_Image6(self,Name = "3000002.jpg"):
        self.label = QLabel(self)
        self.label.resize(181,181)
        self.pm = QPixmap(Name)
        self.label.setPixmap(self.pm)
        self.label.move(670,450)
        self.label.show() 
        return Name[0:7]    
 
class ItemAddedPage(QDialog):
    def __init__(self,user,ReturnPage):
        self.user = user
        self.ReturnPage = ReturnPage
        super(ItemAddedPage,self).__init__()
        uic.loadUi("UIs\ItemAddedPage.ui",self)        
        self.Back_Button.clicked.connect(lambda: self.GoToWindow(ReturnPage))
        
    def GoToWindow(self, window):
        SpoiledEGG.removeWidget(SpoiledEGG.currentWidget())
        SpoiledEGG.addWidget(window)
        SpoiledEGG.setCurrentIndex(0)    
       
class CartPage(QDialog):
    def __init__(self,user):
        self.user = user
        super(CartPage,self).__init__()
        uic.loadUi("UIs\CartPage.ui",self)
        self.Account_Button.clicked.connect(lambda: self.clickedAccount(user))
        self.Forums_Button.clicked.connect(self.load_Forum)
        self.HomePage_Button.clicked.connect(self.load_HomePage)
        
        #Create forLayout
        formLayout = QFormLayout()
        
        #Create groupBox
        groupBox = QGroupBox()
        groupBox.setStyleSheet("QGroupBox { border: 4px solid rgba(116,103,137,1); background-color: white;}")
        groupBox.setLayout(formLayout)
        
        cur = Current_Cart(user)
        i = -1
        self.itemHolder = []
        self.Cart = []
        self.Sum = 0
        for (item) in cur:
            i += 1
            self.itemHolder.append(item[1])
            #Create item title and Add to cart button
            self.Row = QHBoxLayout()
            self.LayoutItems = QVBoxLayout()
            #------------Item_Name-------------------------
            self.Name_of_Item = QPushButton()
            self.Name_of_Item.setStyleSheet("background-color: rgb(170, 0, 255);")
            self.LayoutItems.addWidget(self.Name_of_Item)
            #-------------Delete---------------------------
            self.Cart.append(QPushButton("Delete from Cart")) # Label for title
            self.Cart[i].setStyleSheet("background-color: rgb(170, 170, 255);")
            self.Cart[i].clicked.connect(lambda ch, i=i: self.load_Cart(self.itemHolder[i],user))
            self.LayoutItems.addWidget(self.Cart[i])
            #-------------Price----------------------------
            self.Price = QLabel()
            self.Price.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.Price.setAlignment(QtCore.Qt.AlignCenter)
            self.Price.setFont(QFont('Times',20))
            self.Price.setText('$'+str(item[3]))
            self.Sum = self.Sum + (item[3])*(item[4])
            #-------------Occurence-------------------------
            self.Occurence = QLabel()
            self.Occurence.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.Occurence.setAlignment(QtCore.Qt.AlignRight)
            self.Occurence.setText("In Cart: " + str(item[4]))
            self.Occurence.setFont(QFont('Times',20))
            #combine widgets
            self.Row.addLayout(self.LayoutItems)
            self.Row.addWidget(self.Price)
            self.Row.addWidget(self.Occurence)
            #Create label for image
            TLabel = QLabel()
            pm = QPixmap(str(item[1])+".jpg")
            TLabel.setPixmap(pm)
            self.Name_of_Item.setText(item[2])
            formLayout.addRow(TLabel,self.Row)
        
        if not(Current_Cart(self.user).fetchall()):
            self.Checkout_Button.setEnabled(False)
        else:    
            self.Checkout_Button.clicked.connect(lambda: self.load_Checkout(self.Sum))
        
        #Adjust Scroll Area 
        self.Item_ScrollArea.setWidget(groupBox)
        self.Item_ScrollArea.setFixedWidth(701)
        self.Item_ScrollArea.setFixedHeight(431) 
        
        self.Total_Sum_Button.setText(str(self.Sum))
        self.Total_Sum_Button.setAlignment(QtCore.Qt.AlignCenter)
        self.Total_Sum_Button.setFont(QFont('Times',20))
        
        #Items button
        self.Monitors_Button.clicked.connect(self.load_Monitors)
        self.CPU_Button.clicked.connect(self.load_CPU)
        self.GPU_Button.clicked.connect(self.load_GPU)
        self.PSU_Button.clicked.connect(self.load_PSU)
        self.Storage_Button.clicked.connect(self.load_Storage)
        self.Memory_Button.clicked.connect(self.load_Memory)
        self.Motherboard_Button.clicked.connect(self.load_Motherboard)
        self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
        self.Software_Button.clicked.connect(self.load_Software)
        self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
        self.Laptops_Button.clicked.connect(self.load_Laptops)
     

    def clickedAccount(self, userID):
        AccountDetailUI = AccountDetail(userID,SpoiledEGG,HomePage(userID))
        self.GoToWindow(AccountDetailUI)

    def load_Checkout(self,Sum):
        info = GetPaymentInfo(self.user)
        if info[0] == "" and info[1][0] == 0:
            self.GoToWindow(NoCheckOut(self.user,CartPage(self.user)))
        else:
            self.GoToWindow(CheckOutPage(self.user,HomePage(self.user),CartPage(self.user),Sum))
        
    def load_HomePage(self):
        self.GoToWindow(HomePage(self.user))
        
    def load_Monitors(self):
        self.GoToWindow(ItemsPage(self.user,"Monitors"))   
        
    def load_CPU(self):
        self.GoToWindow(ItemsPage(self.user,"CPU"))
        
    def load_GPU(self):
        self.GoToWindow(ItemsPage(self.user,"GPU"))
            
    def load_PSU(self):
        self.GoToWindow(ItemsPage(self.user,"PSU"))
        
    def load_Storage(self):
        self.GoToWindow(ItemsPage(self.user,"Storage"))

    def load_Memory(self):
        self.GoToWindow(ItemsPage(self.user,"Memory"))
        
    def load_Motherboard(self):
        self.GoToWindow(ItemsPage(self.user,"Motherboard")) 
        
    def load_PC_Cases(self):
        self.GoToWindow(ItemsPage(self.user,"PC_Cases"))
        
    def load_Software(self):
        self.GoToWindow(ItemsPage(self.user,"Software"))
            
    def load_Prebuilds(self):
        self.GoToWindow(ItemsPage(self.user,"Prebuilds"))    

    def load_Laptops(self):
        self.GoToWindow(ItemsPage(self.user,"Laptops"))    
        
    def load_Cart(self,Item_ID,ID):
        connection = Connect_to_Mariadb()
        cur = connection.cursor()
        cur.execute("SELECT Occurence FROM Spoiled_Cart WHERE ID = ? AND Item_ID = ?;",(ID,Item_ID))
        item = cur.fetchone()
        if item[0] == 1:
            cur.execute("DELETE FROM Spoiled_Cart WHERE ID =? AND Item_ID = ?",(ID,Item_ID))
        else:
            cur.execute("UPDATE Spoiled_Cart SET Occurence = ? WHERE ID = ? AND Item_ID = ?;",(item[0]-1,ID,Item_ID))
        connection.commit()
        self.GoToWindow(CartPage(ID))
        connection.close()
        
    def load_Forum(self):
        FrontPageUI = HomePage(self.user)
        ForumUI = ForumWindow(1, "GPU", self.user, SpoiledEGG, FrontPageUI)
        self.GoToWindow(ForumUI)
        
    def GoToWindow(self, window):
        SpoiledEGG.removeWidget(SpoiledEGG.currentWidget())
        SpoiledEGG.addWidget(window)
        SpoiledEGG.setCurrentIndex(0)    
        
class ItemsPage(QDialog): # Type = Monitor,GPU,CPU,Motherboard,PSU,PC_Cases,Memory,Storage,Software,Prebuilds,Laptops
    def __init__(self,user,Type):
        self.user = user
        self.Type = Type
        super(ItemsPage,self).__init__()
        uic.loadUi("UIs\ItemsPage.ui",self)
        if user != 0:
            self.Loggout_Button.setText("Loggout")
            self.Loggout_Button.clicked.connect(lambda: self.clickedLoginNOutBtn(user)) 
            self.Account_Button.clicked.connect(lambda: self.clickedAccount(user))
            self.Cart_Button.clicked.connect(self.load_Cart)
        else:  
            self.Account_Button.setEnabled(False)
            self.Loggout_Button.clicked.connect(lambda: self.clickedLoginNOutBtn(user))
            self.Cart_Button.setEnabled(False)
            
        self.Forums_Button.clicked.connect(self.load_Forum)
        self.HomePage_Button.clicked.connect(self.load_HomePage)
        
        #Create forLayout
        formLayout = QFormLayout()
        
        #Create groupBox
        groupBox = QGroupBox()
        groupBox.setStyleSheet("QGroupBox { border: 4px solid rgba(116,103,137,1); background-color: white;}")
        groupBox.setLayout(formLayout)
        
        i = -1
        self.Cart = []
        self.itemHolder = []
        if Type == "Monitors":
            self.Title.setText("Monitors")
            self.Highlighter_for_Parts.move(30,100)
            
            cur = Current_Monitors()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480) 
            
            #Filter
            
            # Pages we can switch to
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)            
        elif Type == "CPU":
            self.Title.setText("CPU")
            self.Highlighter_for_Parts.move(110,100)
            cur = Current_CPU()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480)
            
            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)            
        elif Type == "GPU":
            self.Title.setText("GPU")
            self.Highlighter_for_Parts.move(190,100)
            cur = Current_GPU()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480) 

            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)                        
        elif Type == "PSU":
            self.Title.setText("PSU")
            self.Highlighter_for_Parts.move(270,100)
            cur = Current_PSU()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480) 

            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)            
        elif Type == "Storage":
            self.Title.setText("Storage")
            self.Highlighter_for_Parts.move(350,100)
            cur = Current_Storage()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480)
            
            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)           
        elif Type == "Memory":
            self.Title.setText("Memory")
            self.Highlighter_for_Parts.move(430,100)
            cur = Current_Memory()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480) 

            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)    
        elif Type == "Motherboard":
            self.Title.setText("Motherboard")
            self.Highlighter_for_Parts.move(510,100)
            cur = Current_Motherboard()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480)
            
            # Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)       
        elif Type == "PC_Cases":
            self.Title.setText("PC_Cases")
            self.Highlighter_for_Parts.move(590,100)
            cur = Current_PC_Cases()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480)        
       
            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)    
        elif Type == "Software":
            self.Title.setText("Software")
            self.Highlighter_for_Parts.move(670,100)
            cur = Current_Software()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480) 
                
            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)    
        elif Type == "Prebuilds":
            self.Title.setText("Prebuilds")
            self.Highlighter_for_Parts.move(750,100)
            cur = Current_Prebuilds()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480)
            
            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Laptops_Button.clicked.connect(self.load_Laptops)
        elif Type == "Laptops":
            self.Title.setText("Laptops")
            self.Highlighter_for_Parts.move(830,100)
            cur = Current_Laptops()
            for (Item) in cur:
                i += 1
                self.itemHolder.append(Item[0])
                #Create item title and Add to cart button
                self.LayoutItems = QVBoxLayout()
                #Add to cart
                self.Cart.append(QPushButton("Add to Cart")) # Description is made as button for check out
                self.Cart[i].setStyleSheet("background-color: rgb(153, 204, 255);")
                self.Cart[i].clicked.connect(lambda ch, i=i: self.addToCart(self.itemHolder[i],user))
                self.LayoutItems.addWidget(self.Cart[i])
                if self.user == False:
                    self.Cart[i].setEnabled(False)
                #For each item - make title and description
                self.Name_of_Item = QLabel() # Description is made as button for check out
                self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
                self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
                self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
                self.LayoutItems.addWidget(self.Name_of_Item)
                #-------------Description---------------------------
                self.Description = QLabel() # Label for title
                self.Description.setStyleSheet("background-color: rgb(170, 170, 255);")
                self.Description.setAlignment(QtCore.Qt.AlignCenter)
                self.LayoutItems.addWidget(self.Description)
                #Create label for image
                TLabel = QLabel()
                pm = QPixmap(str(Item[0])+".jpg")
                TLabel.setPixmap(pm)
                self.Name_of_Item.setText(Item[1])
                self.Description.setText(Item[4])
                formLayout.addRow(TLabel,self.LayoutItems)  
            
            #Adjust Scroll Area 
            self.Item_ScrollArea.setWidget(groupBox)
            self.Item_ScrollArea.setFixedWidth(701)
            self.Item_ScrollArea.setFixedHeight(480)
            
            #Pages we can switch to
            self.Monitors_Button.clicked.connect(self.load_Monitors)
            self.CPU_Button.clicked.connect(self.load_CPU)
            self.GPU_Button.clicked.connect(self.load_GPU)
            self.PSU_Button.clicked.connect(self.load_PSU)
            self.Storage_Button.clicked.connect(self.load_Storage)
            self.Memory_Button.clicked.connect(self.load_Memory)
            self.Motherboard_Button.clicked.connect(self.load_Motherboard)
            self.PC_Cases_Button.clicked.connect(self.load_PC_Cases)
            self.Software_Button.clicked.connect(self.load_Software)
            self.Prebuilds_Button.clicked.connect(self.load_Prebuilds)
            self.Laptops_Button.clicked.connect(self.load_Laptops)
     
    def load_Cart(self):
        self.GoToWindow(CartPage(self.user))

    def addToCart(self,Item_ID,ID):
        cur = GetItemInfo(Item_ID)
        Name = cur[1]
        Price = cur[6]
        connection = Connect_to_Mariadb()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Spoiled_Cart WHERE ID = ? AND Item_ID = ?",(ID,Item_ID))
        item = cursor.fetchone()
        if item is None:
            cursor.execute("INSERT INTO Spoiled_Cart(ID,Item_ID,Name,Price,Occurence) VALUES(?,?,?,?,?)",(ID,int(Item_ID),Name,Price,1))
            connection.commit() 
        else:
            cursor.execute("UPDATE Spoiled_Cart SET Occurence = ? WHERE ID = ? AND Item_ID = ?;",(item[4]+1,ID,Item_ID))
            connection.commit()
        connection.close()    
        self.GoToWindow(ItemAddedPage(self.user,ItemsPage(self.user,self.Type)))
        
    def load_HomePage(self):
        self.GoToWindow(HomePage(self.user))
        
    def load_Monitors(self):
        self.GoToWindow(ItemsPage(self.user,"Monitors"))   
        
    def load_CPU(self):
        self.GoToWindow(ItemsPage(self.user,"CPU"))
        
    def load_GPU(self):
        self.GoToWindow(ItemsPage(self.user,"GPU"))
            
    def load_PSU(self):
        self.GoToWindow(ItemsPage(self.user,"PSU"))
        
    def load_Storage(self):
        self.GoToWindow(ItemsPage(self.user,"Storage"))

    def load_Memory(self):
        self.GoToWindow(ItemsPage(self.user,"Memory"))
        
    def load_Motherboard(self):
        self.GoToWindow(ItemsPage(self.user,"Motherboard")) 
        
    def load_PC_Cases(self):
        self.GoToWindow(ItemsPage(self.user,"PC_Cases"))
        
    def load_Software(self):
        self.GoToWindow(ItemsPage(self.user,"Software"))
            
    def load_Prebuilds(self):
        self.GoToWindow(ItemsPage(self.user,"Prebuilds"))    

    def load_Laptops(self):
        self.GoToWindow(ItemsPage(self.user,"Laptops"))    
           
    def load_Forum(self):
        FrontPageUI = HomePage(self.user)
        ForumUI = ForumWindow(1, "GPU", self.user, SpoiledEGG, FrontPageUI)
        self.GoToWindow(ForumUI)
    
    def clickedLoginNOutBtn(self, userID): ## COMPLETE
        #if someone clicks login botton with a valid userID, then that
        #means they want to log out, so when userID is not 0, we call frontpage(0),
        if userID != False:
            self.GoToWindow(HomePage())
        else:
            self.GoToWindow(LoginScreenWindow(SpoiledEGG,HomePage))
    
    def clickedAccount(self, userID):
        AccountDetailUI = AccountDetail(userID,SpoiledEGG,HomePage(userID))
        self.GoToWindow(AccountDetailUI)
    
    def GoToWindow(self, window):
        SpoiledEGG.removeWidget(SpoiledEGG.currentWidget())
        SpoiledEGG.addWidget(window)
        SpoiledEGG.setCurrentIndex(0)    

class NoCheckOut(QMainWindow):
    def __init__(self,user,ReturnPage):
        self.user = user
        self.ReturnPage = ReturnPage
        super(NoCheckOut,self).__init__()
        uic.loadUi(r"UIs\NoCheckOutPage.ui",self)        
        self.Back_Button.clicked.connect(lambda: self.GoToWindow(ReturnPage))
        
    def GoToWindow(self, window):
        SpoiledEGG.removeWidget(SpoiledEGG.currentWidget())
        SpoiledEGG.addWidget(window)
        SpoiledEGG.setCurrentIndex(0)

class CheckedOut(QMainWindow):
    def __init__(self,user):
        self.user = user
        super(CheckedOut,self).__init__()
        uic.loadUi("UIs\CheckedOutPage.ui",self)        
        self.HomePage_Button.clicked.connect(lambda: self.GoToWindow(HomePage(self.user)))
        self.Shipper_Label.setText(GetUsername(GetShipper(self.user)))
        Delete_Cart(self.user)
        
    def GoToWindow(self, window):
        SpoiledEGG.removeWidget(SpoiledEGG.currentWidget())
        SpoiledEGG.addWidget(window)
        SpoiledEGG.setCurrentIndex(0)

class CheckOutPage(QMainWindow):
    def __init__(self,user,HomePage,CartPage,Sum):
        self.user = user
        self.HomePage = HomePage
        self.CartPage = CartPage
        self.Sum = Sum
        super(CheckOutPage,self).__init__()
        uic.loadUi("UIs\CheckOutPage.ui",self)
        self.Back_to_Cart_Button.clicked.connect(self.load_Cart)
        self.CheckOut_Button.clicked.connect(self.load_Checkout)

        #Create forLayout
        formLayout = QFormLayout()
        
        #Create groupBox
        groupBox = QGroupBox()
        groupBox.setStyleSheet("QGroupBox { border: 4px solid rgba(116,103,137,1); background-color: white;}")
        groupBox.setLayout(formLayout)
        
        cur = Current_Cart(user)
        i = -1
        self.itemHolder = []
        self.Cart = []
        self.Sum = 0
        for (item) in cur:
            i += 1
            self.itemHolder.append(item[1])
            #Create item title and Add to cart button
            self.Row = QHBoxLayout()
            #------------Item_Name-------------------------
            self.Name_of_Item = QLabel()
            self.Name_of_Item.setAlignment(QtCore.Qt.AlignCenter)
            self.Name_of_Item.setFont(QFont('Times',20,weight = QtGui.QFont.Bold))
            self.Name_of_Item.setStyleSheet("background-color: rgb(255, 153, 255); border: 3px solid rgb(153,51,255);")
            #-------------Price----------------------------
            self.Price = QLabel()
            self.Price.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.Price.setAlignment(QtCore.Qt.AlignCenter)
            self.Price.setFont(QFont('Times',20))
            self.Price.setText('$'+str(item[3]))
            self.Sum = self.Sum + (item[3])*(item[4])
            #-------------Occurence-------------------------
            self.Occurence = QLabel()
            self.Occurence.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.Occurence.setAlignment(QtCore.Qt.AlignRight)
            self.Occurence.setText("In Cart: " + str(item[4]))
            self.Occurence.setFont(QFont('Times',20))
            #combine widgets
            self.Row.addWidget(self.Name_of_Item)
            self.Row.addWidget(self.Price)
            self.Row.addWidget(self.Occurence)
            #Create label for image
            TLabel = QLabel()
            pm = QPixmap(str(item[1])+".jpg")
            TLabel.setPixmap(pm)
            self.Name_of_Item.setText(item[2])
            formLayout.addRow(TLabel,self.Row)
           
        #Adjust Scroll Area 
        self.Item_ScrollArea.setWidget(groupBox)
        
        self.Total_Sum_Button.setText(str(self.Sum))
        self.Total_Sum_Button.setAlignment(QtCore.Qt.AlignCenter)
        self.Total_Sum_Button.setFont(QFont('Times',20))

    def load_Checkout(self):
        info = GetPaymentInfo(self.user)
        if info[0] == "" and info[1][0] == 0:
            self.GoToWindow(NoCheckOut(self.user,CartPage(self.user)))
        if info[0] != "":
            self.GoToWindow(CheckedOut(self.user))
        elif info[1] < self.Sum:
            self.GoToWindow(NoCheckOut(self.user,CartPage(self.user)))
        else:
            Charge_Customer(self.user,self.Sum)

    def load_Cart(self):
        self.GoToWindow(CartPage(self.user))
            
    def GoToWindow(self, window):
        SpoiledEGG.removeWidget(SpoiledEGG.currentWidget())
        SpoiledEGG.addWidget(window)
        SpoiledEGG.setCurrentIndex(0)    

app = QApplication(sys.argv)
SpoiledEGG = QtWidgets.QStackedWidget()
SpoiledEGG.setFixedHeight(700)
SpoiledEGG.setFixedWidth(940)

HP = HomePage()
SpoiledEGG.addWidget(HP)
SpoiledEGG.show()
app.exec_()