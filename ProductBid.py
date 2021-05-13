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
from DBAction import GetProduct, InsertBid, FindCompany, FindEmployee, GetBids, AcceptBid, FindBidder

productPerPage = 8
class ProductBidWindow(QMainWindow):

    def __init__(self, widget, UserID, Item_ID, typeOfBid, BiddingWindowBackUp):
        super(ProductBidWindow, self).__init__()
        loadUi("UIs/BiddingHistory.ui",self)
        self.typeOfBid = typeOfBid
        self.BiddingWindowBackUp = BiddingWindowBackUp
        self.Item_ID = Item_ID
        self.UserID = UserID
        self.widget = widget
        self.UserIDPrefix = int(str(UserID)[0])
        self.LoadBids(0, 1)
        self.ShipBtn.clicked.connect(lambda: self.switchBidType("Shipper"))
        self.RetaBtn.clicked.connect(lambda: self.switchBidType("Retailer"))
        self.listWidget.itemDoubleClicked.connect(self.BidAction)
        self.BackBtn.clicked.connect(lambda: self.GoToWindow(BiddingWindowBackUp))

    def BidAction(self, item):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Decisions decisions!')
        box.setText(item.text())
        box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        print(buttonY)
        buttonY.setText('Accept this bid')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('Go back')
        box.exec_()
        if box.clickedButton() == buttonY:
            bidderID = item.whatsThis()
            AcceptBid(self.Item_ID, bidderID, self.typeOfBid)
            self.listWidget.clear()




    def switchBidType(self, typeOfBid):
        self.GoToWindow(ProductBidWindow(self.widget, self.UserID, self.Item_ID, typeOfBid, self.BiddingWindowBackUp))


    def LoadBids(self, nextOrprevious, GoTo):
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

                for bid in GetBids(self.Item_ID, startIndex, productPerPage, self.typeOfBid):
                    title = str(bid[2]) + ": $" + str(bid[3]) + ", at time: " + str(bid[4])
                    if len(title) > 50:
                        post_preview = title[0:50].replace("\n", " ") + "..."
                    else:
                        post_preview = title[0:60].replace("\n", " ")
                    item = QListWidgetItem(post_preview)
                    item.setFont(font)
                    bidderID = FindBidder(bid[2])[0]
                    item.setWhatsThis(str(bidderID))
                    self.listWidget.addItem(item)

    def GoToWindow(self, window):
            #it is assumed that the widget has only one on the stack
            #never use this if there are multiple ui loaded to the stack widget
            self.widget.removeWidget(self.widget.currentWidget())
            self.widget.addWidget(window)
            self.widget.setCurrentIndex(0)


