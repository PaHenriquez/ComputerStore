#Refactor common functions(go_to_front_page)
# Password isnt checked when change request is made

# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=undefined-variable
import sys
import mariadb
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from DBRAction import FindPayment,FindAddressAndStoreCredit,FindUser
from DBRAction import Update_Data, Insert_New_Payment, FindPassword
#from DBAction import FindAddressAndStoreCredit
#from DBAction import FindUser
#from DBAction import Update_Data,Insert_New_Payment,SelectUser
#from DBAction import Insert_New_Payment


class AccountDetail(QMainWindow):

    def __init__(self,UserID,widget,FrontPageUI):
        self.widget = widget
        self.userID = UserID
        self.FrontPageUI = FrontPageUI

        super(AccountDetail,self).__init__()
        loadUi("UIs/AccountDetail.ui",self)

        HistoryUi = AccountHistory(self.widget,self.FrontPageUI)
        self.FrontpageBtn.clicked.connect(lambda: self.GoToWindow(self.FrontPageUI))
        self.PurHisBtn.clicked.connect(lambda: self.GoToWindow(HistoryUi))

        self.FillInInfo()
        self.GETITDONE.clicked.connect(self.ModifyInfo)

    def FillInInfo(self):
        result = FindUser(self.userID)
        self.UsernameLineEdit.setText(result[1])
        self.EmailLineEdit.setText(result[2])
        self.PhoneLineEdit.setText(result[4])
        result = FindAddressAndStoreCredit(self.userID)
        self.AddressLineEdit.setText(result[1])
        self.StoreCreditLineEdit.setText("$"+str(result[2]/100))
        result = FindPayment(self.userID)

        # If payment info not found, it doesn't present payment info on account detail screen
        
        if(result != False):
            self.BankCardLineEdit.setText(
                ' '.join([str(result[1])[i:i+4] for i in range(0, 16, 4)]))
            self.BankNameLineEdit.setText(result[2])
            self.BillAddressLineEdit.setText(result[3])
        
            

    def ModifyInfo(self):

        password = FindPassword(self.userID)

        if(self.ConfirmPass.text() != password):
            self.GETITDONE.setText("Try again")
            self.ConfirmPass.clear()
        else:
            if(self.NewEmailLineEdit.text()):
                Update_Data('Users', 'Email',self.NewEmailLineEdit.text(), self.userID)
            
            if(self.NewPhoneLineEdit.text()):
                Update_Data('Users', 'Phone_Number',self.NewPhoneLineEdit.text(), self.userID)
            
            if(self.NewPasswordLineEdit.text()):
                Update_Data('Users', 'Password',self.NewPasswordLineEdit.text(), self.userID)
            
            if(self.NewAddressLineEdit.text()):
                Update_Data('Customer', 'Address',self.NewAddressLineEdit.text(), self.userID)

            result = FindPayment(self.userID)

            if(result == False):
                Insert_New_Payment(self.userID, self.NewBankCardLineEdit.text(),\
                    self.NewBankNameLineEdit.text(), self.NewBillAddressLineEdit.text())
            else:
                if(self.NewBankCardLineEdit.text()):
                    Update_Data('Payment', 'Payment_Card',self.NewBankCardLineEdit.text(), self.userID)
                
                if(self.NewBankNameLineEdit.text()):
                    Update_Data('Payment', 'Name_On_Card',self.NewBankNameLineEdit.text(), self.userID)
                    
                if(self.NewBillAddressLineEdit.text()):
                    Update_Data('Payment', 'Billing_Address',self.NewBillAddressLineEdit.text(), self.userID)

            self.FrontPageUI.clickedAccount(self.userID)


    def GoToWindow(self, window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)

class AccountHistory(QMainWindow):

    def __init__(self,userId,widget):
        self.userId = userId
        self.widget = widget
        super(AccountHistory,self).__init__()
        loadUi("UIs/InfoHistory.ui",self)

        self.PurHisBtn.clicked.connect(lambda:self.GoToWindow(self.widget))

        self.loadOrderHistory()
        self.comboBox.activated.connect(lambda: self.loadOrderHistory())

        self.loadCommentHistory()
        self.comboBox_2.activated.connect(lambda: self.loadCommentHistory())


    def loadOrderHistory(self):

        order_model = QtGui.QStandardItemModel(1, 1)
        order_model.setHorizontalHeaderLabels(['Date', 'Item', 'Qty'])

        for row, text in enumerate(["CPU", 'GPU', 'CPU2', 'RAM2']):
            item = QtGui.QStandardItem(text)
            order_model.setItem(row, 1, item)

        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(order_model)
        filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(self.comboBox.currentIndex())

        self.lineEdit.textChanged.connect(filter_proxy_model.setFilterRegExp)

        table = self.tableView
        table.setModel(filter_proxy_model)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def loadCommentHistory(self):

        comment_model = QtGui.QStandardItemModel(1,1)
        comment_model.setHorizontalHeaderLabels(['Date','Id','Type','Comment'])

        for row,text in enumerate(['comment 1','blah','test2','jds']):
            item = QtGui.QStandardItem(text)
            comment_model.setItem(row,3,item)

        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(comment_model)
        filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(self.comboBox_2.currentIndex())

        self.lineEdit_2.textChanged.connect(filter_proxy_model.setFilterRegExp)

        table = self.tableView_2
        table.setModel(filter_proxy_model)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def GoToWindow(self,window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)
