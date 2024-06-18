import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2
import io

class Ui_AddProduct(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", 
                                     dbname="postgres", 
                                     user="postgres.oxzprkjuxnjgnfihweyj", 
                                     password="Milliondollarbaby123", 
                                     port=6543)
        self.cur = self.conn.cursor()
        self.image_data = None

    def add_new_product(self):
        product_name = self.lineEdit.text()
        price = self.lineEdit_2.text()
        quantity = self.lineEdit_3.text()
        category = self.comboBox.currentText()
        thickness = self.thickness_lineEdit.text()
        rollsize_width = self.rollsize_input_width.text()
        rollsize_length = self.rollsize_input_length.text()
        product_image = self.image_data

        roll_size = f"{rollsize_width} x {rollsize_length}"

        if not all([product_name, price, quantity, category, product_image]):
            missing_fields = []
            if not product_name:
                missing_fields.append("Product Name")
            if not price:
                missing_fields.append("Price")
            if not quantity:
                missing_fields.append("Quantity")
            if not category:
                missing_fields.append("Category")
            if not product_image:
                missing_fields.append("Product Image")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Please input all required fields:\n{', '.join(missing_fields)}")
            msg.setWindowTitle("Required Fields")
            msg.exec_()
            return

        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setText("Add to product list?")
        confirm_msg.setWindowTitle("Confirmation")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = confirm_msg.exec_()

        if result == QMessageBox.Yes:
            # Save image to a folder (e.g., 'images')
            image_filename = f"{product_name}.png"  # Adjust filename as needed
            image_path = os.path.join('images', image_filename)
            with open(image_path, 'wb') as f:
                f.write(self.image_data)

            # Insert product into database
            sql = """
                INSERT INTO PRODUCT (PROD_NAME, PROD_PRICE, PROD_QUANTITY, PROD_CATEGORY, 
                                     PROD_THICKNESS, PROD_ROLL_SIZE, PROD_IMAGE)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            try:
                self.cur.execute(sql, (product_name, price, quantity, category, thickness, roll_size, self.image_data))
                self.conn.commit()
                print("Product added successfully!")
            except psycopg2.Error as e:
                print(f"Error inserting product: {e}")
                self.conn.rollback()

    def add_new_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaledToWidth(191))  # Display image in QLabel

            with open(file_name, "rb") as image_file:
                self.image_data = image_file.read()

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
        self.category_label.setGeometry(QtCore.QRect(360, 100, 66, 16))
        self.category_label.setObjectName("category_label")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(360, 120, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.thickness_lineEdit = QtWidgets.QLineEdit(self.frame)
        self.thickness_lineEdit.setGeometry(QtCore.QRect(360, 170, 80, 20))
        self.thickness_lineEdit.setObjectName("thickness_lineEdit")
        self.thickness_label = QtWidgets.QLabel(self.frame)
        self.thickness_label.setGeometry(QtCore.QRect(360, 150, 81, 16))
        self.thickness_label.setObjectName("thickness_label")
        self.thickness_oz = QtWidgets.QLabel(self.frame)
        self.thickness_oz.setGeometry(QtCore.QRect(445, 170, 60, 20))
        self.thickness_oz.setObjectName("thickness_oz")
        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.clicked.connect(AddProduct.close)
        self.Cancel.setGeometry(QtCore.QRect(360, 370, 96, 31))
        self.Cancel.setObjectName("Cancel")
        font_cancel = QtGui.QFont()
        font_cancel.setFamily("Arial")
        font_cancel.setPointSize(10)
        font_cancel.setBold(True)        
        self.Cancel.setFont(font_cancel)
        self.AddOrder_3 = QtWidgets.QPushButton(self.frame)
        self.AddOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddOrder_3.clicked.connect(self.add_new_product)
        self.AddOrder_3.clicked.connect(AddProduct.close)
        self.AddOrder_3.setGeometry(QtCore.QRect(470, 370, 91, 31))
        self.AddOrder_3.setObjectName("AddOrder_3")
        font_add_product = QtGui.QFont()
        font_add_product.setFamily("Arial")
        font_add_product.setPointSize(10)
        font_add_product.setBold(True)
        self.AddOrder_3.setFont(font_add_product)        
        self.rollsize_label = QtWidgets.QLabel(self.frame)
        self.rollsize_label.setGeometry(QtCore.QRect(80, 260, 76, 16))
        self.rollsize_label.setObjectName("rollsize_label")
        self.rollsize_input_width = QtWidgets.QLineEdit(self.frame)
        self.rollsize_input_width.setGeometry(QtCore.QRect(80, 280, 40, 20))
        self.rollsize_input_width.setObjectName("rollsize_input_width")
        self.optional_label = QtWidgets.QLabel(self.frame)
        self.optional_label.setGeometry(QtCore.QRect(200, 280, 100, 20))
        font_optional = QtGui.QFont()
        font_optional.setFamily("Arial")
        font_optional.setPointSize(10)
        self.optional_label.setFont(font_optional)
        self.optional_label.setStyleSheet("color: #CCAA00;")
        self.optional_label2 = QtWidgets.QLabel(self.frame)
        self.optional_label2.setGeometry(QtCore.QRect(490, 170, 113, 20))
        font_optional = QtGui.QFont()
        font_optional.setFamily("Arial")
        font_optional.setPointSize(10)
        self.optional_label2.setFont(font_optional)
        self.optional_label2.setStyleSheet("color: #CCAA00;")
        self.rollsize_label.setObjectName("rollsize_label")
        self.label_times = QtWidgets.QLabel(self.frame)
        self.label_times.setGeometry(QtCore.QRect(130, 280, 16, 20))  
        self.label_times.setObjectName("label_times")
        font = QtGui.QFont()
        font.setBold(True) 
        self.label_times.setFont(font)
        self.label_times.setText("X")
        self.rollsize_input_length = QtWidgets.QLineEdit(self.frame)
        self.rollsize_input_length.setGeometry(QtCore.QRect(145, 280, 40, 20))  
        self.rollsize_input_length.setObjectName("rollsize_input_length")
        self.image_label = QtWidgets.QLabel(self.frame)
        self.image_label.setGeometry(QtCore.QRect(360, 210, 200, 96))
        self.image_label.setFrameShape(QtWidgets.QFrame.Box)
        self.image_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.Image = QtWidgets.QPushButton(self.frame)
        self.Image.clicked.connect(self.add_new_image)
        self.Image.setGeometry(QtCore.QRect(360, 310, 200, 31))
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
        self.thickness_oz.setText(_translate("AddProduct", "ounces."))
        self.Cancel.setText(_translate("AddProduct", "Cancel"))
        self.AddOrder_3.setText(_translate("AddProduct", "Add Product"))
        self.rollsize_label.setText(_translate("AddProduct", "Rollsize"))
        self.optional_label.setText(_translate("AddProduct", "(optional)"))
        self.optional_label2.setText(_translate("AddProduct", "(optional)"))
        self.comboBox.setItemText(0, _translate("AddProduct", "Large Format Tarpulin "))
        self.comboBox.setItemText(1, _translate("AddProduct", "Vinyl Sticker Printin"))
        self.comboBox.setItemText(2, _translate("AddProduct", "Laser Printing for papers and Stickers"))
        self.comboBox.setItemText(3, _translate("AddProduct", "T-shirt printing "))
        self.Image.setText(_translate("AddProduct", "Select Image"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    AddProduct = QDialog()
    ui = Ui_AddProduct()
    ui.setupUi(AddProduct)
    AddProduct.show()
    sys.exit(app.exec_())
