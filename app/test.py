import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("Login.ui", self)
        




# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()  # allows pages to switch
#widget.setFixedHeight(650)
widget.setFixedWidth(940)


main_window = MainWindow()  # loads store page
widget.addWidget(main_window)

widget.show()

sys.exit(app.exec_())

