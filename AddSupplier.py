import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2

class Ui_AddSupplier(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", 
                                     dbname="postgres", 
                                     user="postgres.oxzprkjuxnjgnfihweyj", 
                                     password="Milliondollarbaby123", 
                                     port=6543)
        self.cur = self.conn.cursor()

    def add_new_supplier(self):
        sup_name = self.lineEdit.text()
        sup_email = self.emailLineEdit.text()
        sup_contact = self.contactLineEdit.text()
        sup_address = self.addressLineEdit.text()
        sup_country = self.countryComboBox.currentText()

        if not all([sup_name, sup_email, sup_contact, sup_address, sup_country]):
            missing_fields = []
            if not sup_name:
                missing_fields.append("Supplier Name")
            if not sup_email:
                missing_fields.append("Email Address")
            if not sup_contact:
                missing_fields.append("Contact")
            if not sup_address:
                missing_fields.append("Address")
            if not sup_country:
                missing_fields.append("Country")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Please input all required fields:\n{', '.join(missing_fields)}")
            msg.setWindowTitle("Required Fields")
            msg.exec_()
            return

        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setText("Add this supplier?")
        confirm_msg.setWindowTitle("Confirmation")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = confirm_msg.exec_()

        if result == QMessageBox.Yes:
            # Insert supplier into database
            sql = """
                INSERT INTO SUPPLIER (SUP_NAME, SUPPLIER_EMAIL, SUP_CONTACT, SUP_ADDRESS, SUP_COUNTRY)
                VALUES (%s, %s, %s, %s, %s)
                """
            try:
                self.cur.execute(sql, (sup_name, sup_email, sup_contact, sup_address, sup_country))
                self.conn.commit()
                self.show_message("Success", "Data saved successfully.")
                self.close()

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


    def setupUi(self, AddSupplier):
        AddSupplier.setObjectName("AddSupplier")
        AddSupplier.resize(640, 480)
        AddSupplier.setFixedSize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        AddSupplier.setSizePolicy(sizePolicy)
        self.frame = QtWidgets.QFrame(AddSupplier)
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
            "    background-color: #CD2E2E;\n"
            "}\n"
            "QPushButton#edit_cat{    \n"
            "    color: rgb(255, 255, 255);\n"
            "    background-color: #1049ad;\n"
            "}\n"
            "QPushButton{    \n"
            "    color: rgb(255, 255, 255);\n"
            "    background-color: #202020;\n"
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
        self.AddOrder.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))  

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(130, 100, 150, 16))
        self.label.setObjectName("label")
        self.label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))  
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(130, 120, 300, 30))
        self.lineEdit.setMaxLength(300)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(QtGui.QFont("Arial", 12))  

        self.emailLineEdit = QtWidgets.QLineEdit(self.frame)
        self.emailLineEdit.setGeometry(QtCore.QRect(130, 175, 300, 30))
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.emailLabel = QtWidgets.QLabel(self.frame)
        self.emailLabel.setGeometry(QtCore.QRect(130, 155, 76, 16))
        self.emailLabel.setObjectName("emailLabel")
        self.emailLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold)) 
        self.emailLineEdit.setFont(QtGui.QFont("Arial", 12))  

        self.contactLineEdit = QtWidgets.QLineEdit(self.frame)
        self.contactLineEdit.setGeometry(QtCore.QRect(130, 230, 200, 30))
        self.contactLineEdit.setObjectName("contactLineEdit")
        self.contactLabel = QtWidgets.QLabel(self.frame)
        self.contactLabel.setGeometry(QtCore.QRect(130, 210, 81, 16))
        self.contactLabel.setObjectName("contactLabel")
        self.contactLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.contactLineEdit.setFont(QtGui.QFont("Arial", 12))  

        self.addressLabel = QtWidgets.QLabel(self.frame)
        self.addressLabel.setGeometry(QtCore.QRect(130, 280, 76, 16))
        self.addressLabel.setObjectName("addressLabel")
        self.addressLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))  
        self.addressLineEdit = QtWidgets.QLineEdit(self.frame)
        self.addressLineEdit.setGeometry(QtCore.QRect(130, 300, 200, 30))
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.addressLineEdit.setFont(QtGui.QFont("Arial", 12))

        self.countryLabel = QtWidgets.QLabel(self.frame)
        self.countryLabel.setGeometry(QtCore.QRect(130, 350, 76, 16))
        self.countryLabel.setObjectName("countryLabel")
        self.countryLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.countryComboBox = QtWidgets.QComboBox(self.frame)
        self.countryComboBox.setGeometry(QtCore.QRect(130, 370, 113, 30))
        self.countryComboBox.setObjectName("countryComboBox")
        self.countryComboBox.setFont(QtGui.QFont("Arial", 12))

        countries = [
            "Philippines", "Argentina", "Australia", "Austria", "Belgium", "Brazil", "Canada", 
            "China", "Denmark", "Egypt", "Finland", "France", "Germany", "Greece", 
            "India", "Indonesia", "Ireland", "Israel", "Italy", "Japan", "Kenya", 
            "Mexico", "Netherlands", "New Zealand", "Nigeria", "Norway", "Poland", 
            "Portugal", "Russia", "Saudi Arabia", "South Africa", "South Korea", 
            "Spain", "Sweden", "Switzerland", "Thailand", "Turkey", "Ukraine", "United Arab Emirates", 
            "United Kingdom", "United States", "Vietnam"
        ]
        self.countryComboBox.addItems(countries)

        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.clicked.connect(AddSupplier.close)
        self.Cancel.setGeometry(QtCore.QRect(300, 370, 96, 31))
        self.Cancel.setObjectName("Cancel")
        font_Cancel = QtGui.QFont()
        font_Cancel.setFamily("Arial")
        font_Cancel.setPointSize(10)
        font_Cancel.setBold(True)
        self.Cancel.setFont(font_Cancel) 

        self.AddOrder_3 = QtWidgets.QPushButton(self.frame)
        self.AddOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddOrder_3.clicked.connect(self.add_new_supplier)
        self.AddOrder_3.setGeometry(QtCore.QRect(410, 370, 110, 31))
        self.AddOrder_3.setObjectName("AddOrder_3")
        font_Add = QtGui.QFont()
        font_Add.setFamily("Arial")
        font_Add.setPointSize(10)
        font_Add.setBold(True)
        self.AddOrder_3.setFont(font_Add) 

        self.retranslateUi(AddSupplier)
        QtCore.QMetaObject.connectSlotsByName(AddSupplier)

        AddSupplier.setTabOrder(self.lineEdit, self.emailLineEdit)
        AddSupplier.setTabOrder(self.emailLineEdit, self.contactLineEdit)
        AddSupplier.setTabOrder(self.contactLineEdit, self.addressLineEdit)
        AddSupplier.setTabOrder(self.addressLineEdit, self.countryComboBox)
        AddSupplier.setTabOrder(self.countryComboBox, self.Cancel)
        AddSupplier.setTabOrder(self.Cancel, self.AddOrder_3)

    def retranslateUi(self, AddSupplier):
        _translate = QtCore.QCoreApplication.translate
        AddSupplier.setWindowTitle(_translate("AddSupplier", "Add Supplier"))
        self.AddOrder.setText(_translate("AddSupplier", "Add Supplier"))
        self.label.setText(_translate("AddSupplier", "Supplier Name"))
        self.emailLabel.setText(_translate("AddSupplier", "Email"))
        self.contactLabel.setText(_translate("AddSupplier", "Contact"))
        self.addressLabel.setText(_translate("AddSupplier", "Address"))
        self.countryLabel.setText(_translate("AddSupplier", "Country"))
        self.Cancel.setText(_translate("AddSupplier", "Cancel"))
        self.AddOrder_3.setText(_translate("AddSupplier", "Add Supplier"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    AddSupplier = QDialog()
    ui = Ui_AddSupplier()
    ui.setupUi(AddSupplier)
    AddSupplier.show()
    sys.exit(app.exec_())
