from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2

class Ui_AddProduct(object):

    def __init__(self):
        # PostgreSQL connection
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", dbname="postgres", user="postgres.oxzprkjuxnjgnfihweyj", 
                                     password="Milliondollarbaby123", port=6543)
        self.cur = self.conn.cursor()

    def add_new_product(self):
        pass
    
    def add_new_image(self):
        pass

    def setupUi(self, AddProduct):
        AddProduct.setObjectName("AddProduct")
        AddProduct.resize(640, 480)
        self.frame = QtWidgets.QFrame(AddProduct)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.frame.setStyleSheet("QFrame{\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"QLabel#AddOrder{\n"
"    font-size: 25px;\n"
"}\n"
"QLineEdit{\n"
"    width: 200px;\n"
"}\n"
"QPushButton#Cancel{    \n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #202020;\n"
"}\n"
"QPushButton{    \n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #CD2E2E;\n"
"}\n"
"QPushButton#Image{    \n"
"    color: black;\n"
"    background-color: dirty white;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.AddOrder = QtWidgets.QLabel(self.frame)
        self.AddOrder.setGeometry(QtCore.QRect(35, 30, 161, 26))
        self.AddOrder.setObjectName("AddOrder")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, 100, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 120, 111, 20))
        self.lineEdit.setMaxLength(300)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 175, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(80, 155, 76, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 230, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(80, 210, 81, 16))
        self.label_3.setObjectName("label_3")
        self.category_label = QtWidgets.QLabel(self.frame)
        self.category_label.setGeometry(QtCore.QRect(400, 100, 66, 16))
        self.category_label.setObjectName("category_label")
        self.thickness_lineEdit = QtWidgets.QLineEdit(self.frame)
        self.thickness_lineEdit.setGeometry(QtCore.QRect(400, 190, 113, 20))
        self.thickness_lineEdit.setObjectName("thickness_lineEdit")
        self.thickness_label = QtWidgets.QLabel(self.frame)
        self.thickness_label.setGeometry(QtCore.QRect(400, 170, 81, 16))
        self.thickness_label.setObjectName("thickness_label")
        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.clicked.connect(AddProduct.close)
        self.Cancel.setGeometry(QtCore.QRect(354, 360, 96, 31))
        self.Cancel.setObjectName("Cancel")
        self.AddOrder_3 = QtWidgets.QPushButton(self.frame)
        self.AddOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddOrder_3.clicked.connect(self.add_new_product)
        self.AddOrder_3.clicked.connect(AddProduct.close)
        self.AddOrder_3.setGeometry(QtCore.QRect(475, 360, 91, 31))
        self.AddOrder_3.setObjectName("AddOrder_3")
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setGeometry(QtCore.QRect(80, 260, 76, 16))
        self.label_14.setObjectName("label_14")
        self.rollsize_input = QtWidgets.QLineEdit(self.frame)
        self.rollsize_input.setGeometry(QtCore.QRect(80, 280, 40, 20))
        self.rollsize_input.setObjectName("rollsize_input")
        self.label_times = QtWidgets.QLabel(self.frame)
        self.label_times.setGeometry(QtCore.QRect(130, 280, 16, 20))  
        self.label_times.setObjectName("label_times")
        font = QtGui.QFont()
        font.setBold(True) 
        self.label_times.setFont(font)
        self.label_times.setText("X")
        self.rollsize_input2 = QtWidgets.QLineEdit(self.frame)
        self.rollsize_input2.setGeometry(QtCore.QRect(145, 280, 40, 20))  
        self.rollsize_input2.setObjectName("rollsize_input2")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(400, 120, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.Image = QtWidgets.QPushButton(self.frame)
        self.Image.clicked.connect(self.add_new_image)
        self.Image.clicked.connect(AddProduct.close)
        self.Image.setGeometry(QtCore.QRect(365, 240, 191, 96))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("static/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Image.setIcon(icon)
        self.Image.setIconSize(QtCore.QSize(20, 20))
        self.Image.setObjectName("Image")
        self.retranslateUi(AddProduct)
        QtCore.QMetaObject.connectSlotsByName(AddProduct)

    def retranslateUi(self, AddProduct):
        _translate = QtCore.QCoreApplication.translate
        AddProduct.setWindowTitle(_translate("AddProduct", "Dialog"))
        self.AddOrder.setText(_translate("AddProduct", "Add Product"))
        self.label.setText(_translate("AddProduct", "Product Name"))
        self.label_2.setText(_translate("AddProduct", "Price"))
        self.label_3.setText(_translate("AddProduct", "Quantity"))
        self.category_label.setText(_translate("AddProduct", "Category"))
        self.thickness_label.setText(_translate("AddProduct", "Thickness"))
        self.Cancel.setText(_translate("AddProduct", "Cancel"))
        self.AddOrder_3.setText(_translate("AddProduct", "Add Product"))
        self.label_14.setText(_translate("AddProduct", "Rollsize"))
        self.comboBox.setItemText(0, _translate("AddProduct", "Large Format Tarpulin "))
        self.comboBox.setItemText(1, _translate("AddProduct", "Vinyl Sticker Printin"))
        self.comboBox.setItemText(2, _translate("AddProduct", "Laser Printing for papers and Stickers"))
        self.comboBox.setItemText(3, _translate("AddProduct", "T-shirt printing "))
        self.Image.setText(_translate("AddProduct", "Image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddProduct = QtWidgets.QDialog()
    ui = Ui_AddProduct()
    ui.setupUi(AddProduct)
    AddProduct.show()
    sys.exit(app.exec_())
