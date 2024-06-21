from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2

class Ui_UpdateProduct(object):
    
    def __init__(self, prod_id):
        # PostgreSQL connection   
        super(Ui_UpdateProduct, self).__init__()     
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", dbname="postgres", user="postgres.oxzprkjuxnjgnfihweyj", 
                                     password="Milliondollarbaby123", port=6543)
        self.cur = self.conn.cursor()
        self.prod_id = prod_id

    def save_data(self):
        # Get data from UI elements
        prod_name = self.lineEdit.text().strip()
        prod_price = self.priceLineEdit.text().strip()
        prod_quantity = self.quantityLineEdit.text().strip()
        prod_thickness = self.thicknessLineEdit.text().strip()
        rollsize_width = self.rollsizeLineEdit1.text()
        rollsize_height = self.rollsizeLineEdit2.text()
        prod_rollSize = (f'{rollsize_width} X {rollsize_height}')
        # Validate input data
        if not (prod_name and prod_price and prod_quantity):
            self.show_message("Error", "Please fill all the fields.")
            return

        try:
            # Update product details
            sql_update_product = """
            UPDATE PRODUCT 
            SET PROD_NAME = %s, PROD_PRICE = %s, PROD_QUANTITY = %s, PROD_ROLL_SIZE = %s, PROD_THICKNESS = %s
            WHERE PROD_ID = %s
            """
            self.cur.execute(sql_update_product, (prod_name, prod_price, prod_quantity, prod_rollSize, prod_thickness, self.prod_id))
            self.conn.commit()

            self.show_message("Success", "Product updated successfully.")
        except psycopg2.Error as e:
            self.conn.rollback()  # Roll back transaction on error
            error_message = f"Error saving data: {e.pgcode} - {e.pgerror}"
            self.show_message("Error", error_message) 

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def setupUi(self, UpdateProduct):
        UpdateProduct.setObjectName("UpdateProduct")
        UpdateProduct.resize(640, 480)
        UpdateProduct.setFixedSize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        UpdateProduct.setSizePolicy(sizePolicy)

        self.frame = QtWidgets.QFrame(UpdateProduct)
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
        self.AddOrder.setGeometry(QtCore.QRect(35, 30, 191, 26))
        self.AddOrder.setObjectName("AddOrder")

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, 100, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 120, 111, 20))
        self.lineEdit.setMaxLength(300)
        self.lineEdit.setObjectName("lineEdit")
        
        self.priceLineEdit = QtWidgets.QLineEdit(self.frame)
        self.priceLineEdit.setGeometry(QtCore.QRect(80, 175, 113, 20))
        self.priceLineEdit.setObjectName("priceLineEdit")
        self.priceLabel = QtWidgets.QLabel(self.frame)
        self.priceLabel.setGeometry(QtCore.QRect(80, 155, 76, 16))
        self.priceLabel.setObjectName("priceLabel")

        self.quantityLineEdit = QtWidgets.QLineEdit(self.frame)
        self.quantityLineEdit.setGeometry(QtCore.QRect(80, 230, 113, 20))
        self.quantityLineEdit.setObjectName("quantityLineEdit")
        self.quantityLabel = QtWidgets.QLabel(self.frame)
        self.quantityLabel.setGeometry(QtCore.QRect(80, 210, 81, 16))
        self.quantityLabel.setObjectName("quantityLabel")

        self.rollsizeLineEdit1 = QtWidgets.QLineEdit(self.frame)
        self.rollsizeLineEdit1.setGeometry(QtCore.QRect(80, 335, 40, 20))
        self.rollsizeLineEdit1.setObjectName("rollsizeLineEdit1")
        self.rollsizeLineEdit2 = QtWidgets.QLineEdit(self.frame)
        self.rollsizeLineEdit2.setGeometry(QtCore.QRect(155, 335, 40, 20))
        self.rollsizeLineEdit2.setObjectName("rollsizeLineEdit2")
        self.rollsizeLabel = QtWidgets.QLabel(self.frame)
        self.rollsizeLabel.setGeometry(QtCore.QRect(80, 315, 76, 16))
        self.rollsizeLabel.setObjectName("rollsizeLabel")

        self.label_times = QtWidgets.QLabel(self.frame)
        self.label_times.setGeometry(QtCore.QRect(135, 335, 10, 20))  
        self.label_times.setObjectName("label_times")
        font = QtGui.QFont()
        font.setBold(True) 
        self.label_times.setFont(font)
        self.label_times.setText("X")

        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.clicked.connect(UpdateProduct.close)
        self.Cancel.setGeometry(QtCore.QRect(354, 320, 96, 31))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setObjectName("Cancel")

        self.AddOrder_3 = QtWidgets.QPushButton(self.frame)
        self.AddOrder_3.clicked.connect(self.save_data)
        self.AddOrder_3.clicked.connect(UpdateProduct.close)
        self.AddOrder_3.setGeometry(QtCore.QRect(475, 320, 91, 31))
        self.AddOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddOrder_3.setObjectName("AddOrder_3")

        self.thicknessLabel = QtWidgets.QLabel(self.frame)
        self.thicknessLabel.setGeometry(QtCore.QRect(80, 260, 76, 16))
        self.thicknessLabel.setObjectName("thicknessLabel")
        self.thicknessLineEdit = QtWidgets.QLineEdit(self.frame)
        self.thicknessLineEdit.setGeometry(QtCore.QRect(80, 280, 113, 20))
        self.thicknessLineEdit.setObjectName("thicknessLineEdit")

        self.categoryLabel = QtWidgets.QLabel(self.frame)
        self.categoryLabel.setGeometry(QtCore.QRect(400, 100, 66, 16))
        self.categoryLabel.setObjectName("categoryLabel")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(400, 120, 111, 20))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.Image = QtWidgets.QPushButton(self.frame)
        self.Image.setGeometry(QtCore.QRect(365, 180, 191, 96))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("static/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Image.setIcon(icon)
        self.Image.setIconSize(QtCore.QSize(20, 20))
        self.Image.setObjectName("Image")
        self.Cancel.raise_()
        self.AddOrder_3.raise_()

        self.retranslateUi(UpdateProduct)
        QtCore.QMetaObject.connectSlotsByName(UpdateProduct)

    def retranslateUi(self, UpdateProduct):
        _translate = QtCore.QCoreApplication.translate
        UpdateProduct.setWindowTitle(_translate("UpdateProduct", "Dialog"))
        self.AddOrder.setText(_translate("UpdateProduct", "Update Product"))
        self.label.setText(_translate("UpdateProduct", "Product Name"))
        self.priceLabel.setText(_translate("UpdateProduct", "Price"))
        self.quantityLabel.setText(_translate("UpdateProduct", "Quantity"))
        self.rollsizeLabel.setText(_translate("UpdateProduct", "Roll Size"))
        self.categoryLabel.setText(_translate("UpdateProduct", "Category"))
        self.Cancel.setText(_translate("UpdateProduct", "Cancel"))
        self.AddOrder_3.setText(_translate("UpdateProduct", "Update Product"))
        self.thicknessLabel.setText(_translate("UpdateProduct", "Thickness"))
        self.comboBox.setItemText(0, _translate("UpdateProduct", "Large Format Tarpulin "))
        self.comboBox.setItemText(1, _translate("UpdateProduct", "Vinyl Sticker Printin"))
        self.comboBox.setItemText(2, _translate("UpdateProduct", "Laser Printing for papers and Stickers"))
        self.comboBox.setItemText(3, _translate("UpdateProduct", "T-shirt printing "))
        self.Image.setText(_translate("UpdateProduct", "Image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    prod_id = 1
    UpdateProduct = QtWidgets.QDialog()
    ui = Ui_UpdateProduct(prod_id)
    ui.setupUi(UpdateProduct)
    UpdateProduct.show()
    sys.exit(app.exec_())
