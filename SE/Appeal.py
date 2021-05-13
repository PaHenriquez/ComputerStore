
# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
import mariadb
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from Post import PostWindow
from DBAction import InsertPost, FindUser, getTaboo, AddWarning, CreateAppeal


class AppealWindow(QMainWindow):
    def __init__(self, userID):
        self.userID = userID
        self.username = FindUser(userID)[1]
        super(AppealWindow, self).__init__()
        loadUi("UIs/Appeal.ui", self)
        self.label1.setText("Appeal: {}".format(self.username))
        self.SubmitBtn.clicked.connect(self.submit)
    
    def submit(self):
        content = self.AppealTextEdit.toPlainText()
        if content != "":
            CreateAppeal(self.userID, content)


