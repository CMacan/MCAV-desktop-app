import sys
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('Inventory_test.ui', self)

    def setupUi(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        self.label = QLabel()
        pixmap = QPixmap("static/logo.jpg")
        self.label.setPixmap(pixmap)
        self.label.setFixedSize(51, 41)

        layout.addWidget(self.label)
        layout.addStretch() 

        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())