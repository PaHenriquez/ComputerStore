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
from DBAction import GetPosts, FindUser, GetWarning, GetAppeals
from AppealDetail import AppealDetailWindow

#todo:
# 1. create post
# 2. create comments
# 3. create replies
# 4. sort by date
# 5. Login via forum
appealPerPage = 8


class ViewAppealWindow(QMainWindow):
    def __init__(self, page, widget, previousUI):
        super(ViewAppealWindow, self).__init__()
        self.previousUI = previousUI
        self.widget = widget
        self.page = page
        loadUi("UIs/ViewAppeals.ui", self) 
        self.BackBtn.clicked.connect(lambda: self.GoToWindow(previousUI))
        self.listWidget.itemDoubleClicked.connect(self.EnterAppeal)
        self.LoadAppeals(0, 1)
        self.PreviousB.clicked.connect(lambda: self.LoadAppeals(-1, 0))
        self.NextB.clicked.connect(lambda: self.LoadAppeals(1, 0))
        self.GoToB.clicked.connect(lambda: self.LoadAppeals(0, self.pageInput.text()))





    def EnterAppeal(self, item):
        AppealDetailUI = AppealDetailWindow(int(item.whatsThis()))
        AppealDetailUI.BackBtn.clicked.connect(lambda: self.GoToWindow(ViewAppealWindow(self.page, self.widget, self.previousUI)))
        AppealDetailUI.DenyBtn.clicked.connect(lambda: self.GoToWindow(ViewAppealWindow(self.page, self.widget, self.previousUI)))
        AppealDetailUI.AcceptBtn.clicked.connect(lambda: self.GoToWindow(ViewAppealWindow(self.page, self.widget, self.previousUI)))
        self.GoToWindow(AppealDetailUI) #calls the GoToWindow with the instance that is just created


    # if nexrOrprevious = -1 or 1, then we're clicking next or previous button
    # if the goto button is clicked, then the GoTo argument would be the page to go to
    def LoadAppeals(self, nextOrprevious, GoTo):
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
            startIndex = (currentpage - 1) * appealPerPage
            self.Current_page.setText("Current Page: {}".format(currentpage))
            self.listWidget.clear()
            font = QtGui.QFont()
            font.setPointSize(20)
            APPEALS = GetAppeals(startIndex, appealPerPage)
            if APPEALS == [] and startIndex != 0:
                self.LoadAppeals(0, self.page)
            else:
                for appeal in APPEALS:
                    appeal_preview = appeal[1] + ": " + str(appeal[9])
                    item = QListWidgetItem(appeal_preview)
                    item.setFont(font)
                    item.setWhatsThis(str(appeal[0]))
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

    AppealUI = ViewAppealWindow(1, widget, None)
    widget.addWidget(AppealUI)
    widget.show()
    app.exec_()