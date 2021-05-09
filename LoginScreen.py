# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
#import mariadb
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from DBAction import AttemptLogin,DoesEmailExist


class LoginScreenWindow(QMainWindow):
    
    def __init__(self,widget,FrontPageUI):
        self.FrontPageUI = FrontPageUI
        self.widget = widget
        super(LoginScreenWindow,self).__init__()
        loadUi("UIs/Login3.ui",self)
        RegisUi = RegistrationScreenWindow(self.widget,self.FrontPageUI)
        self.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPageUI(0)))
        self.ContinueBtn.clicked.connect(lambda: self.LoginAction(self.EmailForm.text(),\
            self.PasswordForm.text()))
        self.RegistrationBtn.clicked.connect(lambda: self.GoToWindow(RegisUi))
        
    def LoginAction(self,useremail,password):
        result = AttemptLogin(useremail,password)
        if(result != False):
            self.GoToWindow(self.FrontPageUI(result[0]))
        else:

            if(DoesEmailExist(useremail) == False):
                self.ContinueBtn.setText("Email doesn't exist")
            else:
                self.ContinueBtn.setText("Password is incorrect")


    def GoToWindow(self,window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)

class RegistrationScreenWindow(QMainWindow):
    def __init__(self,widget,FrontPageUI):
        self.FrontPageUI = FrontPageUI
        self.widget = widget
        super(RegistrationScreenWindow,self).__init__()
        loadUi("UIs/Registration2.ui",self)
        self.SignInBtn.clicked.connect(lambda:self.GoToWindow(LoginScreenWindow(self.widget,self.FrontPageUI)))
        self.HomeBtn.clicked.connect(lambda: self.GoToWindow(self.FrontPageUI(0)))

    def GoToWindow(self,window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)
