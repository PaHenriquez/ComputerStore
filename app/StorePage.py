#Todo list
#Refactor common functions(go_to_front_page)

import sys

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        uic.loadUi("FrontPage.ui",self)
        self.LoginBtn.clicked.connect(self.go_to_login_screen)

    def go_to_login_screen(self):
        widget.setCurrentIndex(1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen,self).__init__()
        uic.loadUi("Login.ui",self)
        self.HomeBtn.clicked.connect(self.go_to_front_page)
        self.RegistrationBtn.clicked.connect(self.go_to_registration_screen)

    def go_to_front_page(self):
        widget.setCurrentIndex(0)
    
    def go_to_registration_screen(self):
        widget.setCurrentIndex(2)

class RegistrationScreen(QDialog):
    def __init__(self):
        super(RegistrationScreen,self).__init__()
        uic.loadUi("Registration.ui",self)
        self.HomeBtn.clicked.connect(self.go_to_front_page)
        self.SignInBtn.clicked.connect(self.go_to_login_screen)
    
    def go_to_front_page(self):
        widget.setCurrentIndex(0)
    
    def go_to_login_screen(self):
        widget.setCurrentIndex(1)
    
    

# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()  # allows pages to switch
widget.setFixedWidth(940)
widget.setFixedHeight(700)


main_window = MainWindow()  # loads store page
widget.addWidget(main_window)

login_window = LoginScreen()  # loads login screen
widget.addWidget(login_window)

registration_window = RegistrationScreen() #loads registration screen
widget.addWidget(registration_window)

widget.show()

sys.exit(app.exec_())
