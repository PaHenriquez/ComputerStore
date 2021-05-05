
# pylint: disable=missing-docstring
# pylint: disable=no-name-in-module
# pylint: disable=unused-import
import sys
import mysql.connector as maria
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from Post import PostWindow

#todo:
# 1. create post
# 2. create comments
# 3. create replies
# 4. upvote/downvote
# 5. sort by vote

postPerPage = 9


class ForumWindow(QMainWindow):
    def __init__(self, page, curF, userID, widget, FrontPageUI):
        self.FrontPageUI = FrontPageUI
        self.widget = widget
        super(ForumWindow, self).__init__()
        loadUi("UIs/Forum.ui", self) #this loads the initial forum window
        self.curF = curF
        self.userID = userID
        self.listWidget.setSpacing(10) #this is the spacing between each post
        self.LoadPosts(0, page) #this loads the posts from a particular initial page
        self.PreviousB.clicked.connect(lambda: self.LoadPosts(-1, 0))
        self.NextB.clicked.connect(lambda: self.LoadPosts(1, 0))
        self.GoToB.clicked.connect(lambda: self.LoadPosts(0, self.pageInput.text()))
        self.listWidget.itemDoubleClicked.connect(self.EnterPost)
        self.FrontPageBtn.clicked.connect(lambda: self.GoToWindow(FrontPageUI))
        
    def EnterPost(self, item):
        page = int(self.Current_page.text()[14:])
        PostUI = PostWindow(item, self.curF) #creates an instance of PostWindow
        self.GoToWindow(PostUI) #calls the GoToWindow with the instance that is just created
        PostUI.BackToForumB.clicked.connect(lambda:
            self.GoToWindow(ForumWindow(page, self.curF, self.userID, self.widget, self.FrontPageUI)))
        

    # if nexrOrprevious = -1 or 1, then we're clicking next or previous button
    # if the goto button is clicked, then the GoTo argument would be the page to go to
    def LoadPosts(self, nextOrprevious, GoTo):
        try:
            GoTo = int(GoTo)
        except:
            GoTo = int(self.Current_page.text()[14:])

        if int(self.Current_page.text()[14:]) == 1 and nextOrprevious == -1:
            pass
        else:
            if nextOrprevious == 0 and GoTo > 0:
                currentpage = GoTo
            else:
                currentpage = int(self.Current_page.text()[14:]) + nextOrprevious
            startIndex = (currentpage - 1) * postPerPage
            query= "select * from Post_GPU limit {}, {}".format(startIndex, postPerPage)
            self.curF.execute(query)
            self.Current_page.setText("Current Page: {}".format(currentpage))
            self.listWidget.clear()
            font = QtGui.QFont()
            font.setPointSize(20)
            for post in self.curF:
                if len(post[3]) > 50:
                    post_preview = post[3][0:50].replace("\n", " ") + "..."
                else:
                    post_preview = post[3][0:60].replace("\n", " ")
                item = QListWidgetItem(post_preview)
                item.setFont(font)
                item.setWhatsThis(str(post[0]))

                self.listWidget.addItem(item)

    def GoToWindow(self, window):
        #it is assumed that the widget has only one on the stack
        #never use this if there are multiple ui loaded to the stack widget
        self.widget.removeWidget(self.widget.currentWidget())
        self.widget.addWidget(window)
        self.widget.setCurrentIndex(0)




# cnx = maria.connect(user='root', password='password',host='localhost', database='Forum')
# cur = cnx.cursor(buffered=True)
# app = QApplication(sys.argv)
# ForumUI = ForumWindow(1, None)
# widget = QtWidgets.QStackedWidget()
# widget.setFixedHeight(700)
# widget.setFixedWidth(940)
# widget.addWidget(ForumUI)

# widget.show()
# app.exec_()
