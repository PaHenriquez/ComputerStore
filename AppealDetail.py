# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from Post import PostWindow
from CreatePost import CreatePostWindow
from DBAction import GetPosts, FindUser, GetWarning, DecideAppeal

#todo:
# 1. create post
# 2. create comments
# 3. create replies
# 4. sort by date
# 5. Login via forum
postPerPage = 8

class AppealDetailWindow(QMainWindow):
    def __init__(self, userID):
        super(AppealDetailWindow, self).__init__()
        self.userID = userID
        loadUi("UIs/AppealDetail.ui", self) 
        self.AppealTextEdit.setText(FindUser(userID)[8])
        self.label1.setText("Appeal: {}".format(FindUser(userID)[1]))
        self.DenyBtn.clicked.connect(self.deny)
        self.AcceptBtn.clicked.connect(self.accept)

    def deny(self):
        if self.checkBox.isChecked():
            DecideAppeal(self.userID, 0, 1)
        else:
            DecideAppeal(self.userID, 0, 0)
    def accept(self):
        if self.checkBox.isChecked():
            DecideAppeal(self.userID, 1, 1)
        else:
            DecideAppeal(self.userID, 1, 0)

        

