#Refactor common functions(go_to_front_page)
# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
# pylint: disable=undefined-variable
import sys
import mysql.connector as maria
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from DBAction import FindPayment
from DBAction import FindAddressAndStoreCredit
from DBAction import FindUser





class AccountDetail(QMainWindow):
    def __init__(self, userID, curF, curS, widget, FrontPageUI):
        self.widget = widget
        self.userID = userID
        self.curF = curF
        self.curS = curS
        self.FrontPageUI = FrontPageUI
        super(AccountDetail, self).__init__()
        loadUi("UIs/AccountDetail.ui", self)
        self.FillInInfo()
        self.GETITDONE.clicked.connect(self.ModifyInfo)

    def FillInInfo(self):
        result = FindUser(self.curS, self.userID)
        self.UsernameLineEdit.setText(result[1])
        self.EmailLineEdit.setText(result[2])
        self.PhoneLineEdit.setText(result[4])
        result = FindAddressAndStoreCredit(self.curS, self.userID)
        self.AddressLineEdit.setText(result[2])
        self.StoreCreditLineEdit.setText("$"+str(result[3]/100))
        result = FindPayment(self.curS, self.userID)
        self.BankCardLineEdit.setText(' '.join([str(result[1])[i:i+4] for i in range(0, 16, 4)]))
        self.BankNameLineEdit.setText(result[2])
        self.BillAddressLineEdit.setText(result[3])

    def ModifyInfo(self):
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
        pass
    def GoToWindow(self, window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)