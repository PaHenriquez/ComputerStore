
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
from DBAction import InsertPost, FindUser, getTaboo, AddWarning


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
            naughty = False
            k = 0
            result = getTaboo(k, k + 100)
            fixedtitle = title
            fixedcontent = content
            while result:
                for word in result:
                    if word in title or word in content:
                        length = len(word)
                        fixedtitle = fixedtitle.replace(word, length * "*")
                        fixedcontent = fixedcontent.replace(word, length * "*")
                        naughty = True
                k += 100
                result = getTaboo(k, k + 100)
            if naughty:
                AddWarning(self.userID)



            InsertPost(self.userID, self.subForum, username + ": " + fixedtitle, username + ": " + fixedcontent, username)



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

