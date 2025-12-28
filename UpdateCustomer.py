import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
import psycopg2

class Ui_UpdateCustomer(QObject):
    customer_info_updated = pyqtSignal(str, str, str, str, str)  

    def customer(self):
        from Customer import Ui_Customer_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Customer_2()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()

    def update_customer_info(self):
        from psycopg2 import IntegrityError
        # Get the new information entered by the user
        new_first_name = self.firstNameLineEdit.text()
        new_last_name = self.lastNameLineEdit.text()
        new_phone = self.phoneNumLineEdit.text()
        new_address = self.addressLineEdit.text()
        new_email = self.emailLineEdit.text()

        # Check if any of the fields are empty
        if new_first_name or new_last_name or new_phone or new_address or new_email:
            try:
                # Establish a connection to the PostgreSQL database
                conn = psycopg2.connect(host="aws-1-ap-northeast-2.pooler.supabase.com", dbname="postgres", 
                                     user="postgres.qtfyvvwktvfviudotoxh", password="isy9KwSEmgbTdbxi", 
                                     port=6543)
                cur = conn.cursor()

                # Update the customer information in the database
                sql = """
                UPDATE CUSTOMER
                SET CUS_FNAME = %s, CUS_LNAME = %s, CUS_PHONE = %s, CUS_ADDRESS = %s
                WHERE CUS_EMAIL = %s
                """
                cur.execute(sql, (new_first_name, new_last_name, new_phone, new_address, new_email))
                conn.commit()

                self.show_message("Success", "Customer information updated despite duplicate email.")

                # Close the cursor and connection
                cur.close()
                conn.close()

            except IntegrityError as e:
                conn.rollback()  # Rollback the transaction to handle the error gracefully
                print(f"IntegrityError: {e}")

                # Handle the unique constraint violation here (merge data, update other fields, etc.)
                # Example:
                # You can choose to update other fields when the email already exists
                update_sql = """
                UPDATE CUSTOMER
                SET CUS_FNAME = %s, CUS_LNAME = %s, CUS_PHONE = %s, CUS_ADDRESS = %s
                WHERE CUS_EMAIL = %s
                """
                cur.execute(update_sql, (new_first_name, new_last_name, new_phone, new_address, new_email))
                conn.commit()

                self.show_message("Success", "Customer information updated despite duplicate email.")

                # Close the cursor and connection
                cur.close()
                conn.close()

            except psycopg2.Error as e:
                print(f"Error updating customer information: {e}")

        else:
            print("No changes made. Retaining current customer information.")

        self.customer_info_updated.emit(new_first_name, new_last_name, new_phone, new_address, new_email)
    
    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def setupUi(self, UpdateCustomer):
        UpdateCustomer.setObjectName("UpdateCustomer")
        UpdateCustomer.resize(640, 480)
        UpdateCustomer.setFixedSize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        UpdateCustomer.setSizePolicy(sizePolicy)

        self.frame = QtWidgets.QFrame(UpdateCustomer)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.frame.setStyleSheet("QFrame{\n"
"    background-color: rgb(255, 255, 255);\n"
"}\n"
"QLabel#UpdateCusLabel{\n"
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
        self.UpdateCusLabel = QtWidgets.QLabel(self.frame)
        self.UpdateCusLabel.setGeometry(QtCore.QRect(70, 10, 300, 100))
        self.UpdateCusLabel.setObjectName("UpdateCusLabel")

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
        self.phoneNumLabel.setGeometry(QtCore.QRect(80, 260, 76, 16))
        self.phoneNumLabel.setObjectName("phoneNumLabel")

        self.addressLabel = QtWidgets.QLabel(self.frame)
        self.addressLabel.setGeometry(QtCore.QRect(354, 100, 86, 16))
        self.addressLabel.setObjectName("addressLabel")
        self.addressLineEdit = QtWidgets.QLineEdit(self.frame)
        self.addressLineEdit.setGeometry(QtCore.QRect(354, 120, 220, 25))
        self.addressLineEdit.setObjectName("addressLineEdit")

        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.clicked.connect(UpdateCustomer.close)       
        self.Cancel.setGeometry(QtCore.QRect(354, 360, 96, 31))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setObjectName("Cancel")

        self.AddOrder_3 = QtWidgets.QPushButton(self.frame)
        self.AddOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddOrder_3.clicked.connect(self.update_customer_info)
        self.AddOrder_3.setGeometry(QtCore.QRect(475, 360, 91, 31))
        self.AddOrder_3.setObjectName("AddOrder_3")

        self.retranslateUi(UpdateCustomer)
        QtCore.QMetaObject.connectSlotsByName(UpdateCustomer)

    def retranslateUi(self, UpdateCustomer):
        _translate = QtCore.QCoreApplication.translate
        UpdateCustomer.setWindowTitle(_translate("UpdateCustomer", "Dialog"))
        self.UpdateCusLabel.setText(_translate("UpdateCustomer", "Update Customer"))
        self.firstNameLabel.setText(_translate("UpdateCustomer", "First Name"))
        self.lastNameLabel.setText(_translate("UpdateCustomer", "Last Name"))
        self.phoneNumLabel.setText(_translate("UpdateCustomer", "Phone Numer"))
        self.addressLabel.setText(_translate("UpdateCustomer", "Address"))
        self.Cancel.setText(_translate("UpdateCustomer", "Cancel"))
        self.AddOrder_3.setText(_translate("UpdateCustomer", "Update"))
        self.emailLabel.setText(_translate("UpdateCustomer", "Email Address"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    UpdateCustomer = QtWidgets.QDialog()
    ui = Ui_UpdateCustomer()
    ui.setupUi(UpdateCustomer)
    UpdateCustomer.show()
    sys.exit(app.exec_())
