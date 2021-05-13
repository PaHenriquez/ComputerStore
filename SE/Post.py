
# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from DBAction import GetPostByID, GetCommentByPostID, GetRepliesByCommentID, GetCommentByCommentID, GetWarning
from CreateReply import CreateReplyWindow
from CreateComment import CreateCommentWindow

commentoffsetX = 10
commentoffsetY = 430 - 350
commentDimX = 700
commentDimY = 160
commentdisc = 350

replyoffsetX = 130
replyoffsetY = 620  - 350
replyDimX = 580
replyDimY = 130
replydisc = 350

replycontentoffsetX = 10
replycontentoffsetY = 10
replycontentDimX = 550
replycontentDimY = 70
replycontentdisc = 80

replyBtnoffsetX = 20
replyBtnoffsetY = 270
replyBtnoffDimX = 90
replyBtnoffDimY = 50
replyBtndisc = 350


class PostWindow(QMainWindow):
    def __init__(self, widget, currForum, item, PostID, ForumBackUp):
        super(PostWindow, self).__init__()
        if PostID != False:
            self.PostID = PostID
        else:
            self.PostID = int(item.whatsThis())
        self.widget = widget
        self.item = item
        self.currForum = currForum
        self.naughty = False
        if GetWarning(ForumBackUp.userID) > 2:
            self.naughty = True

        loadUi("UIs/Post.ui", self)
        self.CurrentForumLabel.setText("Current forum: " + currForum)
        self.ForumBackUp = ForumBackUp
        self.BackToForumB.clicked.connect(lambda: self.GoToWindow(ForumBackUp))
        self.AddCommentBtn.clicked.connect(self.CreateComment)
        if self.ForumBackUp.userID == 0 or self.naughty:
            self.AddCommentBtn.setEnabled(False)

        self.LoadPostDetail()
        


    def LoadPostDetail(self):
        post = GetPostByID(self.currForum, self.PostID)

        
        self.Post_title = QtWidgets.QTextEdit(self.scrollAreaThreadContents)
        self.Post_title.setGeometry(QtCore.QRect(10, 10, 351, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Post_title.setFont(font)
        self.Post_title.setObjectName("Post_title")
        self.Post_title.setText(post[0][1])
        self.Post_title.setReadOnly(True)


        comments = GetCommentByPostID(self.currForum, self.PostID)

        postcentent = comments[len(comments) - 1]
        self.post_content = QtWidgets.QTextEdit(self.scrollAreaThreadContents)
        self.post_content.setGeometry(QtCore.QRect(commentoffsetX, commentoffsetY, commentDimX, commentDimY))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.post_content.setFont(font)
        self.post_content.setText(postcentent[1])
        self.post_content.setReadOnly(True)
        self.LoadReply(postcentent[0], 0)



        comments.pop()
        commentCounter = 1
        for comment in comments:
            self.Comment_content = QtWidgets.QTextEdit(self.scrollAreaThreadContents)
            self.Comment_content.setGeometry(QtCore.QRect(commentoffsetX,
                commentoffsetY + commentdisc * commentCounter, commentDimX, commentDimY))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.Comment_content.setFont(font)
            self.Comment_content.setObjectName("Comment_content{}".format(commentCounter))
            self.Comment_content.setText(comment[1])
            self.Comment_content.setReadOnly(True)
            self.LoadReply(comment[0], commentCounter)
            commentCounter += 1
        self.scrollAreaThreadContents.setMinimumHeight(commentoffsetY + commentCounter * commentdisc)



    def LoadReply(self, commentID, commentCounter):
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
        replies = GetRepliesByCommentID(self.currForum, commentID)
        if len(replies) != 0:
            for reply in replies:
                self.reply_content = QtWidgets.QTextEdit(self.scrollAreaReplyContents)
                self.reply_content.setGeometry(QtCore.QRect(replycontentoffsetX,
                    replycontentoffsetY + replycontentdisc * replyCounter, replycontentDimX, replycontentDimY))
                font = QtGui.QFont()
                font.setPointSize(14)
                self.reply_content.setFont(font)
                # self.reply_content.setObjectName("reply_content{}".format(replyCounter))
                self.reply_content.setText(reply[1])
                self.reply_content.setReadOnly(True)
                replyCounter += 1
            self.scrollAreaReplyContents.setMinimumHeight(replycontentoffsetY + replyCounter * replycontentdisc)
        else:
            self.noreply = QtWidgets.QLabel(self.scrollAreaReplyContents)
            self.noreply.setGeometry(QtCore.QRect(replycontentDimX // 2 - 50, replycontentDimY // 2 + 20, 90, 20))
            self.noreply.setText("No reply yet :(")
        self.ReplyBtn = QtWidgets.QPushButton(self.scrollAreaThreadContents)
        self.ReplyBtn.setGeometry(QtCore.QRect(
            replyBtnoffsetX, replyBtnoffsetY + commentCounter * replyBtndisc, replyBtnoffDimX, replyBtnoffDimY))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.ReplyBtn.setFont(font)
        self.ReplyBtn.setText("Add\nReply")
        self.ReplyBtn.setObjectName("ReplyBtn" + str(commentCounter))
        self.ReplyBtn.clicked.connect(lambda: self.CreateReply(commentID))
        if self.ForumBackUp.userID == 0 or self.naughty:
            self.ReplyBtn.setEnabled(False)

    def CreateReply(self, commentID):
        createReplyUI = CreateReplyWindow(self.currForum, commentID, self.ForumBackUp.userID)
        self.GoToWindow(createReplyUI)
        createReplyUI.NevermindBtn.clicked.connect(lambda: 
            self.GoToWindow(PostWindow(self.widget, self.currForum, None, self.PostID, self.ForumBackUp)))
        createReplyUI.PublishBtn.clicked.connect(lambda: 
            self.GoToWindow(PostWindow(self.widget, self.currForum, None, self.PostID, self.ForumBackUp)))


    def CreateComment(self):
        createCommentUI = CreateCommentWindow(self.currForum, self.PostID, self.ForumBackUp.userID)
        self.GoToWindow(createCommentUI)
        createCommentUI.NevermindBtn.clicked.connect(lambda: 
            self.GoToWindow(PostWindow(self.widget, self.currForum, None, self.PostID, self.ForumBackUp)))
        createCommentUI.PublishBtn.clicked.connect(lambda: 
            self.GoToWindow(PostWindow(self.widget, self.currForum, None, self.PostID, self.ForumBackUp)))

    def GoToWindow(self, window):
        #it is assumed that the widget has only one on the stack
        #never use this if there are multiple ui loaded to the stack widget
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)

