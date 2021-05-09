# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
import mariadb
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from DBAction import AttemptLogin


class LoginScreenWindow(QMainWindow):
    
    def __init__(self,cur,widget,FrontPageUI):
        self.FrontPageUI = FrontPageUI
        self.widget = widget
        self.cur = cur
        super(LoginScreenWindow,self).__init__()
        loadUi("UIs/Login3.ui",self)
        #RegisUi = RegistrationScreen()
        self.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPageUI))

    def LoginAction(self,useremail,password):
        result = AttemptLogin(self.cur,useremail,password)
        if(result != False):
            pass
        else:
            self.ContinueBtn.setText("Fail! Try Again?")

    def GoToWindow(self,window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)