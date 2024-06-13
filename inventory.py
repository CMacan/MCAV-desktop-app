import sys
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('Inventory.ui', self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())