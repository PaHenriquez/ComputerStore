
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
from DBAction import InsertPost, FindUser


class CreatePostWindow(QMainWindow):
    def __init__(self, subForum, userID):
        self.subForum = subForum
        self.userID = userID
        super(CreatePostWindow, self).__init__()
        loadUi("UIs/CreatePost.ui", self) #this loads the initial forum window
        self.CurrentForumLabel.setText("Current forum: " + subForum)
        self.PublishBtn.clicked.connect(self.Create)

    def Create(self):
        username = FindUser(self.userID)[1]
        title = self.TitleTextEdit.toPlainText()
        content = self.ContentTextEdit.toPlainText()
        if title != "" and content != "":
            InsertPost(self.userID, self.subForum, username + ": " + title, username + ": " + content, username)



# if __name__ == "__main__":
#     cnx = mariadb.connect(user='root', password='password',host='localhost', database='Forum')
#     cur = cnx.cursor(buffered=True)
#     app = QApplication(sys.argv)
#     widget = QtWidgets.QStackedWidget()
#     widget.setFixedHeight(700)
#     widget.setFixedWidth(940)

#     CreatePostWindow = CreatePostWindow(1,123456)
#     widget.addWidget(CreatePostWindow)
#     widget.show()
#     app.exec_()

