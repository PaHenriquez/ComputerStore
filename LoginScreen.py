# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
#import mariadb
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from random import randint
from DBRAction import AttemptLogin,DoesEmailExist,DoesUsernameExist,FindUser
from DBRAction import Insert_New_User


class LoginScreenWindow(QMainWindow):
    
    def __init__(self,widget,FrontPageUI):
        self.FrontPageUI = FrontPageUI
        self.widget = widget
        super(LoginScreenWindow,self).__init__()
        loadUi("UIs/LoginPage.ui",self)

        RegisUi = RegistrationScreenWindow(self.widget, self.FrontPageUI)

        #Setting up buttons for page navigation on Login Screen
        self.HomeBtn.clicked.connect(lambda: self.GoToWindow(self.FrontPageUI()))
        self.ContinueBtn.clicked.connect(lambda: self.LoginAction(self.EmailForm.text(),self.PasswordForm.text()))
        self.RegistrationBtn.clicked.connect(lambda: self.GoToWindow(RegisUi))
        
        #Setting up buttons for page navigation on Register screen
        #Note1(5/10/21):
        #Widget get lost when passed to RegisterScreen class
        #Causes page navigation from registeration screen to break

        RegisUi.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPageUI()))
        RegisUi.SignInBtn.clicked.connect(lambda: self.GoToWindow(LoginScreenWindow(self.widget,self.FrontPageUI)))
        
        
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
        #print("Login GoToWindowfunction")

class RegistrationScreenWindow(QMainWindow):

    def __init__(self,widget,FrontPageUI):
        self.FrontPageUI = FrontPageUI
        self.widget = widget
        super(RegistrationScreenWindow,self).__init__()
        loadUi("UIs/Registration2.ui",self)

        self.RegisterBtn.clicked.connect(lambda: self.RegisterAction(self.UsernameForm.text(),
            self.EmailForm.text(), self.PasswordForm.text(), self.PasswordReEntryForm.text()))

        #(Note1: 2 lines in question)
        #self.SignInBtn.clicked.connect(lambda:self.GoToWindow(LoginScreenWindow(self.widget,self.FrontPageUI)))
        #self.HomeBtn.clicked.connect(lambda: self.GoToWindow(self.FrontPageUI(0)))

    def RegisterAction(self,username,email,password,password_reentry):
        if(DoesUsernameExist(username) == True):
            self.RegisterBtn.setText("username exist, pick a new username")
        elif(DoesEmailExist(email) == True):
            self.RegisterBtn.setText("Email registered, pick a new email")
        elif(self.PasswordForm.text() != self.PasswordReEntryForm.text()):
            self.RegisterBtn.setText("Passwords does not match")
        elif(username == "" or email == "" or password == "" or password_reentry == ""):
            self.RegisterBtn.setText("Registration form is not complete")
        else:
            id = 6000000 + randint(10000, 90000)
            while(FindUser(id) != False):
                id = 6000000 + randint(10000, 90000)
            #print(id)
            Insert_New_User(id, username, email, password, '0', 'Customer')
            self.RegisterBtn.setText("Successful registeration! Go Login")

            #clears inputs
            self.UsernameForm.clear()
            self.EmailForm.clear()
            self.PasswordForm.clear()
            self.PasswordReEntryForm.clear()

    def GoToWindow(self,window):
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)
        print("Register GoToWindowfunction")