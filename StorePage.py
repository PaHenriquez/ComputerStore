#Todo list
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
from Post import PostWindow
from Forum import ForumWindow
from DBAction import AttemptLogin
from AccountDetail import AccountDetail
from DBAction import Insert_New_User, Insert_New_Payment
from DBAction import AttemptRegistration



class FrontPage(QMainWindow):
    def __init__(self, userID):
        self.userID = userID
        super(FrontPage, self).__init__()
        loadUi("UIs/HomePage.ui",self)

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
            self.GoToWindow(LoginUI)

            # test
            #FrontPageUI = FrontPage(userID)
            #LoginUI = LoginScreenWindow(cur,widget,FrontPageUI)
            #self.GoToWindow(LoginUI)
            #LoginUI.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPageUI))


            #regisUI = RegistrationScreen()
            #LoginUI.RegistrationBtn.clicked.connect(lambda: self.GoToWindow(regisUI))
            #LoginUI.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPage(userID)))
            
        

    def clickedAccount(self, userID):
        FrontPageUI = FrontPage(userID)
        #AccountDetailUI = AccountDetail(userID, curF, curS, widget, FrontPageUI)
        AccountDetailUI = AccountDetail(userID,cur,widget,FrontPageUI)
        self.GoToWindow(AccountDetailUI)
        AccountDetailUI.FrontpageBtn.clicked.connect(lambda: self.GoToWindow(FrontPage(userID)))


    def GoToWindow(self, window):
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(window)
        widget.setCurrentIndex(0)


class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("UIs/Login3.ui", self)
        RegisUi = RegistrationScreen()
        
        self.ContinueBtn.clicked.connect(
            lambda: self.LoginAction(self.EmailForm.text(), self.PasswordForm.text()))
        self.RegistrationBtn.clicked.connect(lambda: self.GoToWindow(RegisUi))
        self.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPage(0)))

    def LoginAction(self, useremail, password):
        result = AttemptLogin(cur, useremail, password)
        if result != False:
            self.GoToWindow(FrontPage(result[0]))
        else:
            self.ContinueBtn.setText("Fail! Try again?")

    def GoToWindow(self, window):
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(window)
        widget.setCurrentIndex(0)

class RegistrationScreen(QMainWindow):
    def __init__(self):
        super(RegistrationScreen,self).__init__()
        loadUi("UIs/Registration2.ui",self)
        self.HomeBtn.clicked.connect(lambda: self.GoToWindow(FrontPage(0)))
        self.SignInBtn.clicked.connect(lambda: self.GoToWindow(LoginScreen()))
        self.RegisterBtn.clicked.connect(lambda: self.RegisterAction(self.UsernameForm.text(),\
            self.EmailForm.text(),self.PasswordForm.text(),self.PasswordReEntryForm.text()))

    def RegisterAction(self,username,email,password,password_reentry):
        result = AttemptRegistration(cur,username,email,password,password_reentry)
        if(result != False):
            self.RegisterBtn.setText("Succesful registeration! Go Login")
        else:
            self.RegisterBtn.setText("Fail! Try again?")

    def GoToWindow(self,window):
        widget.removeWidget(widget.currentWidget())
        widget.addWidget(window)
        widget.setCurrentIndex(0)


def Connect_to_Mariadb():
    connection = mariadb.connect(
        user = "root",
        password = "1234",
        host = "localhost",
        port = 3306,
        database = "SpoiledEgg"
    )
    return connection


#cnxS = mariadb.connect(user='root', password='1234',host='localhost', database='Store')
#curS = cnxS.cursor(buffered=True)
#cnxF = maria.connect(user='root', password='1234',host='localhost', database='Forum')
#curF = cnxF.cursor(buffered=True)


cnx = Connect_to_Mariadb()
cur = cnx.cursor()


#Insert_New_Payment(cur, 1, "00010899", "Snortz", "Nyc")

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.setFixedHeight(700)
widget.setFixedWidth(940)
widget.addWidget(FrontPage(1))
widget.show()
app.exec_()
