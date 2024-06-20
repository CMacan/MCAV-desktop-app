import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2

class Ui_UpdateSupplier(QDialog):
    def __init__(self, sup_id):
        super(Ui_UpdateSupplier, self).__init__()
        # PostgreSQL connection
        self.conn = psycopg2.connect(
            host="aws-0-ap-southeast-1.pooler.supabase.com",
            dbname="postgres",
            user="postgres.oxzprkjuxnjgnfihweyj",
            password="Milliondollarbaby123",
            port=6543
        )
        self.cur = self.conn.cursor()
        self.sup_id = sup_id

    def fetch_supplier_details(self, sup_name):
        try:
            sql_get_supplier = "SELECT SUP_NAME, SUP_EMAIL, SUP_CONTACT, SUP_ADDRESS, SUP_COUNTRY FROM SUPPLIER WHERE SUP_NAME = %s"
            self.cur.execute(sql_get_supplier, (sup_name,))
            result = self.cur.fetchone()
            
            if result:
                self.lineEdit.setText(result[0])
                self.emailLineEdit.setText(result[1])
                self.contactLineEdit.setText(result[2])
                self.addressLineEdit.setText(result[3])
                self.countryComboBox.setCurrentText(result[4])
            else:
                self.show_message("Error", "Supplier not found.")
        except psycopg2.Error as e:
            error_message = f"Error fetching data: {e.pgcode} - {e.pgerror}"
            self.show_message("Error", error_message)

    def save_data(self):
        # Get data from UI elements
        sup_name = self.lineEdit.text().strip()
        sup_email = self.emailLineEdit.text().strip()
        sup_contact = self.contactLineEdit.text().strip()
        sup_address = self.addressLineEdit.text().strip()
        sup_country = self.countryComboBox.currentText()

        # Validate input data
        if not (sup_name and sup_email and sup_contact and sup_address and sup_country):
            self.show_message("Error", "Please fill all the fields.")
            return

        try:
            # Update supplier details using the stored supplier ID
            sql_update_supplier = """
            UPDATE SUPPLIER 
            SET SUP_NAME = %s, SUP_EMAIL = %s, SUP_CONTACT = %s, SUP_ADDRESS = %s, SUP_COUNTRY = %s
            WHERE SUP_ID = %s
            """
            self.cur.execute(sql_update_supplier, (sup_name, sup_email, sup_contact, sup_address, sup_country, self.sup_id))
            self.conn.commit()

            self.show_message("Success", "Supplier updated successfully.")
            
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
        self.AddOrder.setGeometry(QtCore.QRect(35, 30, 200, 26))
        self.AddOrder.setObjectName("AddOrder")
        self.AddOrder.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))  

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(130, 120 - 40, 150, 16))
        self.label.setObjectName("label")
        self.label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(130, 140 - 40, 300, 30))
        self.lineEdit.setMaxLength(300)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(QtGui.QFont("Arial", 12))  

        self.emailLineEdit = QtWidgets.QLineEdit(self.frame)
        self.emailLineEdit.setGeometry(QtCore.QRect(130, 195 - 40, 300, 30))
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.emailLabel = QtWidgets.QLabel(self.frame)
        self.emailLabel.setGeometry(QtCore.QRect(130, 175 - 40, 76, 16))
        self.emailLabel.setObjectName("emailLabel")
        self.emailLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold)) 
        self.emailLineEdit.setFont(QtGui.QFont("Arial", 12))  

        self.contactLineEdit = QtWidgets.QLineEdit(self.frame)
        self.contactLineEdit.setGeometry(QtCore.QRect(130, 250 - 40, 200, 30))
        self.contactLineEdit.setObjectName("contactLineEdit")
        self.contactLabel = QtWidgets.QLabel(self.frame)
        self.contactLabel.setGeometry(QtCore.QRect(130, 230 - 40, 81, 16))
        self.contactLabel.setObjectName("contactLabel")
        self.contactLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.contactLineEdit.setFont(QtGui.QFont("Arial", 12))  

        self.addressLabel = QtWidgets.QLabel(self.frame)
        self.addressLabel.setGeometry(QtCore.QRect(130, 300 - 40, 76, 16))
        self.addressLabel.setObjectName("addressLabel")
        self.addressLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))  
        self.addressLineEdit = QtWidgets.QLineEdit(self.frame)
        self.addressLineEdit.setGeometry(QtCore.QRect(130, 320 - 40, 200, 30))
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.addressLineEdit.setFont(QtGui.QFont("Arial", 12))

        self.countryLabel = QtWidgets.QLabel(self.frame)
        self.countryLabel.setGeometry(QtCore.QRect(130, 370 - 40, 76, 16))
        self.countryLabel.setObjectName("countryLabel")
        self.countryLabel.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.countryComboBox = QtWidgets.QComboBox(self.frame)
        self.countryComboBox.setGeometry(QtCore.QRect(130, 390 - 40, 200, 30))
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
        self.Cancel.setGeometry(QtCore.QRect(350, 410, 96, 31))
        self.Cancel.setObjectName("Cancel")
        font_Cancel = QtGui.QFont()
        font_Cancel.setFamily("Arial")
        font_Cancel.setPointSize(10)
        font_Cancel.setBold(True)
        self.Cancel.setFont(font_Cancel) 

        self.updateSupplier = QtWidgets.QPushButton(self.frame)
        self.updateSupplier.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.updateSupplier.clicked.connect(self.save_data)
        self.updateSupplier.setGeometry(QtCore.QRect(460, 410, 140, 31))
        self.updateSupplier.setObjectName("updateSupplier")
        font_Add = QtGui.QFont()
        font_Add.setFamily("Arial")
        font_Add.setPointSize(10)
        font_Add.setBold(True)
        self.updateSupplier.setFont(font_Add) 

        self.retranslateUi(AddSupplier)
        QtCore.QMetaObject.connectSlotsByName(AddSupplier)

        AddSupplier.setTabOrder(self.lineEdit, self.emailLineEdit)
        AddSupplier.setTabOrder(self.emailLineEdit, self.contactLineEdit)
        AddSupplier.setTabOrder(self.contactLineEdit, self.addressLineEdit)
        AddSupplier.setTabOrder(self.addressLineEdit, self.countryComboBox)
        AddSupplier.setTabOrder(self.countryComboBox, self.Cancel)
        AddSupplier.setTabOrder(self.Cancel, self.updateSupplier)

    def retranslateUi(self, AddSupplier):
        _translate = QtCore.QCoreApplication.translate
        AddSupplier.setWindowTitle(_translate("AddSupplier", "Update Supplier"))
        self.AddOrder.setText(_translate("AddSupplier", "Update Supplier"))
        self.label.setText(_translate("AddSupplier", "Supplier Name"))
        self.emailLabel.setText(_translate("AddSupplier", "Email"))
        self.contactLabel.setText(_translate("AddSupplier", "Contact"))
        self.addressLabel.setText(_translate("AddSupplier", "Address"))
        self.countryLabel.setText(_translate("AddSupplier", "Country"))
        self.Cancel.setText(_translate("AddSupplier", "Cancel"))
        self.updateSupplier.setText(_translate("AddSupplier", "Update Supplier"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sup_id = 1
    UpdateSupplier = QDialog()
    ui = Ui_UpdateSupplier(sup_id)
    ui.setupUi(UpdateSupplier)
    UpdateSupplier.show()
    sys.exit(app.exec_())
