from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import  pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox, QDialog
import psycopg2
import re 

class Ui_AddCustomer(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", 
                                     dbname="postgres", 
                                     user="postgres.oxzprkjuxnjgnfihweyj", 
                                     password="Milliondollarbaby123", 
                                     port=6543)
        self.cur = self.conn.cursor()

    def add_new_customer(self):
        cus_fname = self.firstNameLineEdit.text()
        cus_lname = self.lastNameLineEdit.text()
        cus_email = self.emailLineEdit.text()
        cus_contact = self.phoneNumLineEdit.text()
        cus_address = self.addressLineEdit.text()

        if not all([cus_fname, cus_lname, cus_email, cus_contact, cus_address]):
            missing_fields = []
            if not cus_fname:
                missing_fields.append("First Name")
            if not cus_lname:
                missing_fields.append("Last Name")
            if not cus_email:
                missing_fields.append("Email")
            if not cus_contact:
                missing_fields.append("Phone Number")
            if not cus_address:
                missing_fields.append("Address")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Please input all required fields:\n{', '.join(missing_fields)}")
            msg.setWindowTitle("Required Fields")
            msg.exec_()
            return
        
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.match(pat,cus_email):
            pass
        else:
            self.show_message("Invalid", "Invalid Email. Please try again.")
            return
        
        digits_only = re.sub(r'\D', '', cus_contact)
    
        if len(digits_only) == 11:
            pass
        else:
            self.show_message("Invalid","Please enter Eleven(11) digits only starting with 09-")
            return
        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setText("Add this customer?")
        confirm_msg.setWindowTitle("Confirmation")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = confirm_msg.exec_()

        if result == QMessageBox.Yes:
            # Insert customer into database
            sql = """
                INSERT INTO CUSTOMER (CUS_FNAME, CUS_LNAME, CUS_EMAIL, CUS_PHONE, CUS_ADDRESS)
                VALUES (%s, %s, %s, %s, %s)
                """
            try:
                self.cur.execute(sql, (cus_fname, cus_lname, cus_email, cus_contact, cus_address))
                self.conn.commit()
                self.show_message("Success", "Data saved successfully.")
                self.clear_input_fields()

            except psycopg2.Error as e:
                self.conn.rollback()  # Roll back transaction on error
                error_message = f"Error saving data: {e.pgcode} - {e.pgerror}"
                self.show_message("Error", error_message) 

    def clear_input_fields(self):
        self.firstNameLineEdit.clear()
        self.lastNameLineEdit.clear()
        self.emailLineEdit.clear()
        self.phoneNumLineEdit.clear()
        self.addressLineEdit.clear()
        self.addressLineEdit.clear()

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def setupUi(self, AddCustomer):
        AddCustomer.setObjectName("AddCustomer")
        AddCustomer.resize(640, 480)
        AddCustomer.setFixedSize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        AddCustomer.setSizePolicy(sizePolicy)

        self.frame = QtWidgets.QFrame(AddCustomer)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.frame.setStyleSheet("QFrame{\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"QLabel#AddCusLabel{\n"
"    font-size: 25px;\n"
"    font-weight: bold;\n"
"}\n"
"QLabel{\n"
"    font-size: 15px; \n"
"}\n"
"QLineEdit{\n"
"    width: 200px;\n"
"    font-size: 15px;\n"
"}\n"
"QPushButton#Cancel{    \n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #202020;\n"
"}\n"
"QPushButton{    \n"
"    color: rgb(255, 255, 255);\n"
"    background-color: #CD2E2E;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.AddCusLabel = QtWidgets.QLabel(self.frame)
        self.AddCusLabel.setGeometry(QtCore.QRect(70, 10, 300, 100))
        self.AddCusLabel.setObjectName("AddCusLabel")

        self.firstNameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.firstNameLineEdit.setGeometry(QtCore.QRect(80, 120, 200, 25))
        self.firstNameLineEdit.setObjectName("firstNameLineEdit")
        self.firstNameLabel = QtWidgets.QLabel(self.frame)
        self.firstNameLabel.setGeometry(QtCore.QRect(80, 100, 76, 16))
        self.firstNameLabel.setObjectName("firstNameLabel")

        self.lastNameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.lastNameLineEdit.setGeometry(QtCore.QRect(80, 175, 200, 25))
        self.lastNameLineEdit.setObjectName("lineEdit_3")
        self.lastNameLabel = QtWidgets.QLabel(self.frame)
        self.lastNameLabel.setGeometry(QtCore.QRect(80, 155, 81, 16))
        self.lastNameLabel.setObjectName("lastNameLabel")

        self.emailLabel = QtWidgets.QLabel(self.frame)
        self.emailLabel.setGeometry(QtCore.QRect(80, 205, 200, 16))
        self.emailLabel.setObjectName("emailLabel")
        self.emailLineEdit = QtWidgets.QLineEdit(self.frame)
        self.emailLineEdit.setGeometry(QtCore.QRect(80, 225, 200, 25))
        self.emailLineEdit.setObjectName("emailLineEdit")

        self.phoneNumLineEdit = QtWidgets.QLineEdit(self.frame)
        self.phoneNumLineEdit.setGeometry(QtCore.QRect(80, 280, 113, 25))
        self.phoneNumLineEdit.setObjectName("phoneNumLineEdit")
        self.phoneNumLabel = QtWidgets.QLabel(self.frame)
        self.phoneNumLabel.setGeometry(QtCore.QRect(80, 260, 150, 16))
        self.phoneNumLabel.setObjectName("phoneNumLabel")

        self.addressLabel = QtWidgets.QLabel(self.frame)
        self.addressLabel.setGeometry(QtCore.QRect(354, 100, 86, 16))
        self.addressLabel.setObjectName("addressLabel")
        self.addressLineEdit = QtWidgets.QLineEdit(self.frame)
        self.addressLineEdit.setGeometry(QtCore.QRect(354, 120, 220, 25))
        self.addressLineEdit.setObjectName("addressLineEdit")

        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.clicked.connect(AddCustomer.close)       
        self.Cancel.setGeometry(QtCore.QRect(354, 360, 96, 31))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setObjectName("Cancel")

        self.AddOrder_3 = QtWidgets.QPushButton(self.frame)
        self.AddOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddOrder_3.clicked.connect(self.add_new_customer)
        self.AddOrder_3.setGeometry(QtCore.QRect(475, 360, 91, 31))
        self.AddOrder_3.setObjectName("AddOrder_3")

        self.retranslateUi(AddCustomer)
        QtCore.QMetaObject.connectSlotsByName(AddCustomer)

    def retranslateUi(self, AddCustomer):
        _translate = QtCore.QCoreApplication.translate
        AddCustomer.setWindowTitle(_translate("AddCustomer", "Dialog"))
        self.AddCusLabel.setText(_translate("AddCustomer", "Add Customer"))
        self.firstNameLabel.setText(_translate("AddCustomer", "First Name"))
        self.lastNameLabel.setText(_translate("AddCustomer", "Last Name"))
        self.phoneNumLabel.setText(_translate("AddCustomer", "Phone Number"))
        self.addressLabel.setText(_translate("AddCustomer", "Address"))
        self.Cancel.setText(_translate("AddCustomer", "Cancel"))
        self.AddOrder_3.setText(_translate("AddCustomer", "Add"))
        self.emailLabel.setText(_translate("AddCustomer", "Email Address"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddCustomer = QtWidgets.QDialog()
    ui = Ui_AddCustomer()
    ui.setupUi(AddCustomer)
    AddCustomer.show()
    sys.exit(app.exec_())
