#Refactor common functions(go_to_front_page)
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
from DBAction import FindPayment
from DBAction import FindAddressAndStoreCredit
from DBAction import FindUser
from DBAction import Update_Data


class AccountDetail(QMainWindow):

    def __init__(self,UserID,cur,widget,FrontPageUI):
        self.widget = widget
        self.userID = UserID
        self.cur = cur
        self.FrontPageUI = FrontPageUI

        super(AccountDetail,self).__init__()
        loadUi("UIs/AccountDetail.ui",self)
        self.FillInInfo()
        self.GETITDONE.clicked.connect(self.ModifyInfo)

    def FillInInfo(self):
        result = FindUser(self.cur, self.userID)
        self.UsernameLineEdit.setText(result[1])
        self.EmailLineEdit.setText(result[2])
        self.PhoneLineEdit.setText(result[4])
        result = FindAddressAndStoreCredit(self.cur, self.userID)
        self.AddressLineEdit.setText(result[1])
        self.StoreCreditLineEdit.setText("$"+str(result[2]/100))
        result = FindPayment(self.cur, self.userID)

        # If payment info not found, it doesn't present payment info on account detail screen
        
        if(result != False):
            self.BankCardLineEdit.setText(
                ' '.join([str(result[1])[i:i+4] for i in range(0, 16, 4)]))
            self.BankNameLineEdit.setText(result[2])
            self.BillAddressLineEdit.setText(result[3])
        
            

    def ModifyInfo(self):

        print(type(self.userID))
        if(self.NewPhoneLineEdit.text()):
            Update_Data(self.cur,'Users','Phone_Number',self.NewPhoneLineEdit.text(),self.userID)

        if(self.NewEmailLineEdit.text()):
            Update_Data(self.cur,'Users','Email',self.NewEmailLineEdit.text(),self.userID)

        if(self.NewPasswordLineEdit.text()):
            Update_Data(self.cur,'Users','Password',self.NewPasswordLineEdit.text(),self.userID)

        if(self.NewAddressLineEdit.text()):
            Update_Data(self.cur,'Customer','Address',self.NewAddressLineEdit.text(),self.userID)

        if(self.NewBankCardLineEdit.text()):
            Update_Data(self.cur,'Payment','Payment_Card',self.NewBankCardLineEdit.text(),self.userID)

        if(self.NewBankNameLineEdit.text()):
            Update_Data(self.cur,'Payment','Name_On_Card',self.NewBankNameLineEdit.text(),self.userID)

        if(self.NewBillAddressLineEdit.text()):
            Update_Data(self.cur,'Payment','Billing_Address',self.NewBillAddressLineEdit.text(),self.userID)

        self.FrontPageUI.clickedAccount(self.userID)
        
        
        # NewEmailLineEdit
        # NewPhoneLineEdit
        # NewPasswordLineEdit
        # # All_user^
        # NewAddressLineEdit
        # # Customer ^
        # NewBankCardLineEdit
        # NewBankNameLineEdit
        # NewBillAddressLineEdit
        # # Payment ^
        

    def GoToWindow(self, window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)



