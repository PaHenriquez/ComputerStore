
# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
import mysql.connector as maria
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi



commentoffsetX = 10
commentoffsetY = 430 - 350
commentDimX = 700
commentDimY = 160
commentdisc = 350

replyoffsetX = 60
replyoffsetY = 620  - 350
replyDimX = 650
replyDimY = 130
replydisc = 350

replycontentoffsetX = 10
replycontentoffsetY = 10
replycontentDimX = 610
replycontentDimY = 70
replycontentdisc = 80



class PostWindow(QMainWindow):
    def __init__(self, item, cursor):
        super(PostWindow, self).__init__()
        self.cur = cursor
        self.item = item
        super(PostWindow, self).__init__()
        loadUi("UIs/Post.ui", self)
        self.LoadPostDetail()



    def LoadPostDetail(self):
        Post_ID = int(self.item.whatsThis())
        query = "SELECT * FROM Post_GPU WHERE Post_ID = {}".format(Post_ID)
        self.cur.execute(query)
        post = self.cur.fetchall()
        
        self.Post_title = QtWidgets.QTextEdit(self.scrollAreaThreadContents)
        self.Post_title.setGeometry(QtCore.QRect(10, 10, 351, 70))
        self.Post_title.setObjectName("Post_title")
        self.Post_title.setText(post[0][3])
        self.Post_title.setReadOnly(True)


        query = "SELECT * FROM Comment_GPU WHERE Post_ID = {}".format(Post_ID)
        self.cur.execute(query)
        commentCounter = 0
        for comment in self.cur:
            self.Comment_content = QtWidgets.QTextEdit(self.scrollAreaThreadContents)
            self.Comment_content.setGeometry(QtCore.QRect(commentoffsetX,
                commentoffsetY + commentdisc * commentCounter, commentDimX, commentDimY))
            self.Comment_content.setObjectName("Comment_content{}".format(commentCounter))
            self.Comment_content.setText(comment[1])
            self.Comment_content.setReadOnly(True)
            self.LoadReply(comment[0], commentCounter)
            commentCounter += 1
        self.scrollAreaThreadContents.setMinimumHeight(commentoffsetY + commentCounter * commentdisc)



    def LoadReply(self, commentID, commentCounter):
        cnx = maria.connect(user='root', password='password',host='localhost', database='Forum')
        cur = cnx.cursor(buffered=True)
        query = "SELECT * FROM Reply_GPU WHERE Comment_ID = {}".format(commentID)
        cur.execute(query)

        self.scrollAreaReply = QtWidgets.QScrollArea(self.scrollAreaThreadContents)
        self.scrollAreaReply.setGeometry(QtCore.QRect(replyoffsetX,
            replyoffsetY + replydisc * commentCounter, replyDimX, replyDimY))
        self.scrollAreaReply.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollAreaReply.setWidgetResizable(True)
        self.scrollAreaReply.setObjectName("scrollAreaReply")

        self.scrollAreaReplyContents = QtWidgets.QWidget()
        self.scrollAreaReplyContents.setGeometry(QtCore.QRect(0, 0, replyDimX - 12, replyDimY - 2))
        self.scrollAreaReplyContents.setObjectName("scrollAreaReplyContents")

        self.scrollAreaReply.setWidget(self.scrollAreaReplyContents)

        replyCounter = 0
        if cur.rowcount != 0:
            for reply in cur:
                self.reply_content = QtWidgets.QTextEdit(self.scrollAreaReplyContents)
                self.reply_content.setGeometry(QtCore.QRect(replycontentoffsetX,
                    replycontentoffsetY + replycontentdisc * replyCounter, replycontentDimX, replycontentDimY))
                self.reply_content.setObjectName("reply_content{}".format(replyCounter))
                self.reply_content.setText(reply[1])
                self.reply_content.setReadOnly(True)
                replyCounter += 1
            self.scrollAreaReplyContents.setMinimumHeight(replycontentoffsetY + replyCounter * replycontentdisc)
        else:
            self.noreply = QtWidgets.QLabel(self.scrollAreaReplyContents)
            self.noreply.setGeometry(QtCore.QRect(replycontentDimX // 2 - 50, replycontentDimY // 2 + 20, 90, 20))
            self.noreply.setText("No reply yet :(")

