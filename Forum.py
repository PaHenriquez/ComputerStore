
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
from DBAction import GetPosts, FindUser

#todo:
# 1. create post
# 2. create comments
# 3. create replies
# 4. sort by date
# 5. Login via forum
postPerPage = 8


class ForumWindow(QMainWindow):
    def __init__(self, page, currForum, userID, widget, FrontPageUI):
        super(ForumWindow, self).__init__()
        self.FrontPageUI = FrontPageUI
        self.widget = widget
        self.currForum = currForum
        self.userID = userID
        loadUi("UIs/Forum.ui", self) #this loads the initial forum window
        if userID != False:
            self.username = FindUser(userID)[1]
            self.loginas.setText("You're logged in as\n"+str(self.username))
        else:
            self.username = 0     
            self.loginas.setText("You're not\nlogged in!")
            self.NewPostBtn.setEnabled(False)
        
        if currForum == "PCCases":
            self.CurrentForumLabel.setText("Current forum: Cases")
        else:
            self.CurrentForumLabel.setText("Current forum: {}".format(self.currForum))

        self.listWidget.setSpacing(10) #this is the spacing between each post
        self.LoadPosts(0, page) #this loads the posts from a particular initial page
        self.PreviousB.clicked.connect(lambda: self.LoadPosts(-1, 0))
        self.NextB.clicked.connect(lambda: self.LoadPosts(1, 0))
        self.GoToB.clicked.connect(lambda: self.LoadPosts(0, self.pageInput.text()))
        self.listWidget.itemDoubleClicked.connect(self.EnterPost)
        self.HomePageBtn.clicked.connect(lambda: self.GoToWindow(FrontPageUI))
        self.NewPostBtn.clicked.connect(self.CreatePost)
        self.CPUBtn.clicked.connect(lambda: self.SwitchSubforum("CPU"))
        self.GPUBtn.clicked.connect(lambda: self.SwitchSubforum("GPU"))
        self.PSUBtn.clicked.connect(lambda: self.SwitchSubforum("PSU"))
        self.MonitorBtn.clicked.connect(lambda: self.SwitchSubforum("Monitor"))
        self.StorageBtn.clicked.connect(lambda: self.SwitchSubforum("Storage"))
        self.MemoryBtn.clicked.connect(lambda: self.SwitchSubforum("Memory"))
        self.MotherboardBtn.clicked.connect(lambda: self.SwitchSubforum("Motherboard"))
        self.PCCasesBtn.clicked.connect(lambda: self.SwitchSubforum("PCCases"))
        self.SoftwareBtn.clicked.connect(lambda: self.SwitchSubforum("Software"))
        self.PrebuildsBtn.clicked.connect(lambda: self.SwitchSubforum("Prebuild"))
        self.LaptopsBtn.clicked.connect(lambda: self.SwitchSubforum("Laptop"))




    def SwitchSubforum(self, subforum):
        self.GoToWindow(ForumWindow(0, subforum, self.userID, self.widget, self.FrontPageUI))

    def CreatePost(self):
        page = int(self.Current_page.text()[14:])
        
        CreatePostUI = CreatePostWindow(self.currForum, self.userID)
        self.GoToWindow(CreatePostUI)

        CreatePostUI.NevermindBtn.clicked.connect(lambda:
            self.GoToWindow(ForumWindow(page, self.currForum, self.userID, self.widget, self.FrontPageUI)))

        CreatePostUI.PublishBtn.clicked.connect(lambda:
            self.GoToWindow(ForumWindow(page, self.currForum, self.userID, self.widget, self.FrontPageUI)))


    def EnterPost(self, item):
        page = int(self.Current_page.text()[14:])
        ForumBackUp = ForumWindow(page, self.currForum, self.userID, self.widget, self.FrontPageUI)
        PostUI = PostWindow(self.widget, self.currForum, item, False, ForumBackUp) #creates an instance of PostWindow
        self.GoToWindow(PostUI) #calls the GoToWindow with the instance that is just created


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
            self.Current_page.setText("Current Page: {}".format(currentpage))
            self.listWidget.clear()
            font = QtGui.QFont()
            font.setPointSize(20)
            for post in GetPosts(self.currForum, startIndex, postPerPage):
                if len(post[1]) > 50:
                    post_preview = post[1][0:50].replace("\n", " ") + "..."
                else:
                    post_preview = post[1][0:60].replace("\n", " ")
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setFixedHeight(700)
    widget.setFixedWidth(940)

    ForumUI = ForumWindow(1, "GPU", 0, widget, None)
    widget.addWidget(ForumUI)
    widget.show()
    app.exec_()
