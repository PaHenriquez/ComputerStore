# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from DBAction import GetPostByID, InsertCommentByPostID, GetCommentByPostID, FindUser

class CreateCommentWindow(QMainWindow):
    def __init__(self, subForum, PostID, userID):
        self.userID = userID
        self.subForum = subForum
        self.PostID = PostID
        super(CreateCommentWindow, self).__init__()
        loadUi("UIs/CreateComment.ui", self)
        self.CurrentForumLabel.setText("Current forum: " + subForum)
        self.PublishBtn.clicked.connect(self.Create)
        self.PostTitleTextEdit.setText(GetPostByID(subForum, PostID)[0][1])
        self.PostContentTextEdit.setText(GetCommentByPostID(subForum, PostID)[0][1])


    def Create(self):
        username = FindUser(self.userID)[1]
        content = self.CommentContentTextEdit.toPlainText()
        if content != "":
            InsertCommentByPostID(self.subForum, self.PostID, username + ": " + content, username)
            
