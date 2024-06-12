from PyQt5 import QtWidgets, uic, QtGui

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('Inventory.ui', self)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
