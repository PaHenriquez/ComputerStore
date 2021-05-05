#Todo list
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
from Post import PostWindow
from Forum import ForumWindow
from DBAction import AttemptLogin
from AccountDetail import AccountDetail

class FrontPage(QMainWindow):
    def __init__(self, userID):
        self.userID = userID
        super(FrontPage, self).__init__()
        loadUi("UIs/FrontPage.ui",self)

        if userID != False:
            self.LoginNOutBtn.setText("Log me out!")
        self.LoginNOutBtn.clicked.connect(lambda: self.clickedLoginNOutBtn(userID))
        self.ForumBtn.clicked.connect(lambda: self.clickedForum(userID))
        self.AccountDetailBtn.clicked.connect(lambda: self.clickedAccount(userID))


    def clickedForum(self, userID):
        FrontPageUI = FrontPage(userID)
        # why pass 1? it's the page number
        # why pass curF? the forum cursor is necessary to load the posts
        # (unless you make a new one in forum.py)
        # why pass widget? same reason as curF, so we don't create a new widget
        # why pass a new instance of FrontPageUI? so the forumpageUi knows where
        # it came from when it gets deleted when you go into a post, so it can get back
        ForumUI = ForumWindow(1, curF, userID, widget, FrontPageUI)
        self.GoToWindow(ForumUI)
       


    def clickedLoginNOutBtn(self, userID):
        #if someone clicks login botton with a valid userID, then that
        #means they want to log out, so when userID is not 0, we call frontpage(0),
        
        if userID != False:
            self.GoToWindow(FrontPage(0))
        else:
            LoginUI = LoginScreen()
            regisUI = RegistrationScreen()
            self.GoToWindow(LoginUI)

            LoginUI.RegistrationBtn.clicked.connect(lambda: self.GoToWindow(regisUI))
            LoginUI.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPage(userID)))
            
        

    def clickedAccount(self, userID):
        FrontPageUI = FrontPage(userID)
        AccountDetailUI = AccountDetail(userID, curF, curS, widget, FrontPageUI)
        self.GoToWindow(AccountDetailUI)
        AccountDetailUI.FrontpageBtn.clicked.connect(lambda: self.GoToWindow(FrontPage(userID)))


    def GoToWindow(self, window):
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(window)
        widget.setCurrentIndex(1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("UIs/Login.ui", self)
        self.ContinueBtn.clicked.connect(
            lambda: self.LoginAction(self.EmailForm.text(), self.PasswordForm.text()))

    def LoginAction(self, useremail, password):
        result = AttemptLogin(curS, useremail, password)
        if result != False:
            self.GoToWindow(FrontPage(result[0]))
        else:
            self.ContinueBtn.setText("Fail! Try again?")

    def GoToWindow(self, window):
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(window)
        widget.setCurrentIndex(0)

class RegistrationScreen(QDialog):
    def __init__(self):
        super(RegistrationScreen,self).__init__()
        loadUi("UIs/Registration.ui",self)





cnxS = maria.connect(user='root', password='password',host='localhost', database='Store')
curS = cnxS.cursor(buffered=True)
cnxF = maria.connect(user='root', password='password',host='localhost', database='Forum')
curF = cnxF.cursor(buffered=True)
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.setFixedHeight(700)
widget.setFixedWidth(940)
widget.addWidget(FrontPage(123))
widget.show()
app.exec_()