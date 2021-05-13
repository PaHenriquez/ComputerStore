#Refactor common functions(go_to_front_page)
# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=undefined-variable

#changes to DB
#1. change Bid_ID to auto increment
import sys
import mariadb
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from DBAction import GetProduct, InsertBid, FindCompany, FindEmployee
from ProductBid import ProductBidWindow

productPerPage = 8
class BiddingWindow(QMainWindow):

    def __init__(self, widget, page, UserID, productType):
        super(BiddingWindow, self).__init__()
        loadUi("UIs/Bidding.ui",self)
        self.UserIDPrefix = int(str(UserID)[0])
        if self.UserIDPrefix == 1 or self.UserIDPrefix == 2:
            self.listWidget.itemDoubleClicked.connect(self.showBidHistory)
            LoginAs = lambda x: "Manager" if x == 1 else "Employee"
            self.loginas.setText("You're logged in as\n" + LoginAs(self.UserIDPrefix))
        else:
            self.listWidget.itemDoubleClicked.connect(self.showBidDialog)
            self.Company = FindCompany(UserID)[1]
            CompanyType = lambda x: "Retailer" if x == 4 else "Shipper"
            self.CompanyType = CompanyType(self.UserIDPrefix)
            self.loginas.setText("You're logged in as\n"+str(self.Company))
        self.productType = productType
        self.widget = widget
        self.userID = UserID
        self.listWidget.setSpacing(10)
        self.LoadProducts(0, 1)

        self.PreviousB.clicked.connect(lambda: self.LoadProducts(-1, 0))
        self.NextB.clicked.connect(lambda: self.LoadProducts(1, 0))
        self.GoToB.clicked.connect(lambda: self.LoadProducts(0, self.pageInput.text()))
        
        self.CPUBtn.clicked.connect(lambda: self.SwitchSubBid("CPU"))
        self.GPUBtn.clicked.connect(lambda: self.SwitchSubBid("GPU"))
        self.PSUBtn.clicked.connect(lambda: self.SwitchSubBid("PSU"))
        self.MonitorBtn.clicked.connect(lambda: self.SwitchSubBid("Monitor"))
        self.StorageBtn.clicked.connect(lambda: self.SwitchSubBid("Storage"))
        self.MemoryBtn.clicked.connect(lambda: self.SwitchSubBid("Memory"))
        self.MotherboardBtn.clicked.connect(lambda: self.SwitchSubBid("Motherboard"))
        self.PCCasesBtn.clicked.connect(lambda: self.SwitchSubBid("PC_Cases"))
        self.SoftwareBtn.clicked.connect(lambda: self.SwitchSubBid("Software"))
        self.PrebuildsBtn.clicked.connect(lambda: self.SwitchSubBid("Prebuilds"))
        self.LaptopsBtn.clicked.connect(lambda: self.SwitchSubBid("Laptops"))

    def LoadProducts(self, nextOrprevious, GoTo):
        try:
            GoTo = int(GoTo)
        except:
            GoTo = int(self.Current_page.text()[14:])

        if int(self.Current_page.text()[14:]) == 1 and nextOrprevious == -1:
            pass
        else:
            if nextOrprevious == 0 and GoTo > 0:
                currentpage = GoTo
            else:
                currentpage = int(self.Current_page.text()[14:]) + nextOrprevious
            startIndex = (currentpage - 1) * productPerPage
            self.Current_page.setText("Current Page: {}".format(currentpage))
            self.listWidget.clear()
            font = QtGui.QFont()
            font.setPointSize(20)
            for product in GetProduct(self.productType, startIndex, productPerPage):
                title = str(product[0]) + ": " + product[1]
                if len(title) > 50:
                    product_preview = title[0:50].replace("\n", " ") + "..."
                else:
                    product_preview = title[0:60].replace("\n", " ")
                item = QListWidgetItem(product_preview)
                item.setFont(font)
                item.setWhatsThis(str(product[0]))

                self.listWidget.addItem(item)

    def SwitchSubBid(self, productType):
        self.GoToWindow(BiddingWindow(self.widget, 0, self.userID, productType))

    def showBidHistory(self, item):
        page = int(self.Current_page.text()[14:])
        BiddingWindowBackUp = BiddingWindow(self.widget, page, self.userID, self.productType)
        ProductBidUI = ProductBidWindow(self.widget, self.userID, item.whatsThis(), "Shipper", BiddingWindowBackUp)
        self.GoToWindow(ProductBidUI)


    def showBidDialog(self, item):
        dlg = QInputDialog(self)                 
        dlg.setInputMode( QInputDialog.TextInput) 
        dlg.setLabelText("Enter your bid (in dollar amount) for\n{}:".format(item.text()))                        
        dlg.resize(200,500)                             
        dlg.exec_()                                
        try:
            bid = int(dlg.textValue())
            InsertBid(item.whatsThis(), self.Company, self.CompanyType, bid)
        except ValueError:
            pass


    def GoToWindow(self, window):
        #it is assumed that the widget has only one on the stack
        #never use this if there are multiple ui loaded to the stack widget
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setFixedHeight(700)
    widget.setFixedWidth(940)

    # prefix 5 = shipper, 4 = retailer, 1 = manager 2 = employee
    # 5666	Amazon	Shipper
    # 43124	Walmart	Retailer
    # 44444	Target	Retailer
    # 55555	USPS	Shipper
    BiddingUI = BiddingWindow(widget, 0, 222, "GPU")
    widget.addWidget(BiddingUI)
    widget.show()
    app.exec_()