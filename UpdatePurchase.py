import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_UpdatePurchase(object):

    def __init__(self, pur_id):
        # PostgreSQL connection
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", dbname="postgres", user="postgres.oxzprkjuxnjgnfihweyj",
                                     password="Milliondollarbaby123", port=6543)
        self.cur = self.conn.cursor()
        self.pur_id = pur_id

    def save_data(self):
        # Get data from UI elements
        sup_id = self.searchLineEdit.text().strip()
        pur_amount = self.totalLineEdit.text().strip()
        pur_order_date = self.orderDateEdit.date().toString(QtCore.Qt.ISODate)
        pur_prod_name = self.prodNameLineEdit.text().strip()
        pur_thickness = self.thicknessLineEdit.text().strip()
        pur_quantity = self.quantityLineEdit.text().strip()
        pur_rollsize_width = self.rollsizeLineEdit1.text()
        pur_rollsize_height = self.rollsizeLineEdit2.text()
        pur_roll_size = f"{pur_rollsize_width} X {pur_rollsize_height}"

        # Validate input data
        if not (sup_id and pur_amount and pur_order_date and pur_prod_name and pur_quantity):
            self.show_message("Error", "Please fill all the fields.")
            return

        try:
            # Update purchase details using the stored purchase ID
            sql_update_purchase = """
            UPDATE PURCHASE 
            SET SUP_ID = %s, PUR_AMOUNT = %s, PUR_ORDER_DATE = %s, PUR_PRODUCT_NAME = %s,
            PUR_THICKNESS = %s, PUR_QUANTITY = %s, PUR_ROLL_SIZE = %s
            WHERE PUR_ID = %s
            """

            self.cur.execute(sql_update_purchase, (sup_id, pur_amount, pur_order_date, pur_prod_name, pur_thickness, pur_quantity, pur_roll_size, self.pur_id))
            self.conn.commit()

            self.show_message("Success", "Purchase updated successfully.")
            
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

    def search_supplier(self):
        sup_id = self.searchLineEdit.text().strip()
        if not sup_id:
            self.show_message("Error", "Please enter a Supplier ID to search.")
            return

        try:
            self.cur.execute("SELECT SUP_NAME, SUP_EMAIL, SUP_CONTACT, SUP_ADDRESS, SUP_COUNTRY FROM SUPPLIER WHERE SUP_ID = %s", (sup_id,))
            supplier_data = self.cur.fetchone()
            if supplier_data:
                sup_name, sup_email, sup_contact, sup_address, sup_country = supplier_data
                self.lineEdit.setText(sup_name)
                self.emailLineEdit.setText(sup_email)
                self.contactLineEdit.setText(sup_contact)
                self.addressLineEdit.setText(sup_address)
                self.countryLineEdit.setText(sup_country)
            else:
                self.show_message("Not Found", "Supplier ID not found.")
        except psycopg2.Error as e:
            error_message = f"Error fetching data: {e.pgcode} - {e.pgerror}"
            self.show_message("Error", error_message)

    def setupUi(self, UpdatePurchase):
        UpdatePurchase.setObjectName("UpdatePurchase")
        UpdatePurchase.resize(640, 480)
        self.frame = QtWidgets.QFrame(UpdatePurchase)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgb(255, 255, 255);
            }
            QLabel#UpdatePurchase {
                font-size: 25px;
            }
            QLineEdit {
                width: 200px;
            }
            QLineEdit#lineEdit,                     
            QLineEdit#supplierLineEdit, 
            QLineEdit#emailLineEdit, 
            QLineEdit#contactLineEdit, 
            QLineEdit#addressLineEdit,
            QLineEdit#countryLineEdit {
                background-color: #e3e1e1;
                color: black;
            }
            QPushButton#Cancel {
                color: rgb(255, 255, 255);
                background-color: #202020;
            }
                              
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: #CD2E2E;
            }
        """)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.UpdatePurchase = QtWidgets.QLabel(self.frame)
        self.UpdatePurchase.setGeometry(QtCore.QRect(35, 20, 250, 50))
        self.UpdatePurchase.setObjectName("UpdatePurchase")
        font_UpdatePurchase = QtGui.QFont()
        font_UpdatePurchase.setFamily("Arial")
        font_UpdatePurchase.setPointSize(15)
        font_UpdatePurchase.setBold(True)
        self.UpdatePurchase.setFont(font_UpdatePurchase)

        self.searchLineEdit = QtWidgets.QLineEdit(self.frame)
        self.searchLineEdit.setGeometry(QtCore.QRect(80, 90, 111, 20))
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchLabel = QtWidgets.QLabel(self.frame)
        self.searchLabel.setGeometry(QtCore.QRect(80, 70, 111, 16))
        self.searchLabel.setObjectName("searchLabel")

        # Search Button
        self.searchButton = QtWidgets.QPushButton(self.frame)
        self.searchButton.setGeometry(QtCore.QRect(200, 90, 75, 23))
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchButton.setObjectName("searchButton")
        font_search = QtGui.QFont()
        font_search.setFamily("Arial")
        font_search.setPointSize(8)
        font_search.setBold(True)
        self.searchButton.setFont(font_search)
        self.searchButton.clicked.connect(self.search_supplier)  # Connect search button to search method

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, 120, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 140, 111, 20))
        self.lineEdit.setMaxLength(300)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)  # Make read-only

        self.emailLineEdit = QtWidgets.QLineEdit(self.frame)
        self.emailLineEdit.setGeometry(QtCore.QRect(80, 195, 113, 20))
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.emailLineEdit.setReadOnly(True)  # Make read-only
        self.emailLabel = QtWidgets.QLabel(self.frame)
        self.emailLabel.setGeometry(QtCore.QRect(80, 175, 76, 16))
        self.emailLabel.setObjectName("emailLabel")

        self.contactLineEdit = QtWidgets.QLineEdit(self.frame)
        self.contactLineEdit.setGeometry(QtCore.QRect(80, 250, 113, 20))
        self.contactLineEdit.setObjectName("contactLineEdit")
        self.contactLineEdit.setReadOnly(True)  # Make read-only
        self.contactLabel = QtWidgets.QLabel(self.frame)
        self.contactLabel.setGeometry(QtCore.QRect(80, 230, 81, 16))
        self.contactLabel.setObjectName("contactLabel")

        self.addressLabel = QtWidgets.QLabel(self.frame)
        self.addressLabel.setGeometry(QtCore.QRect(80, 280, 76, 16))
        self.addressLabel.setObjectName("addressLabel")
        self.addressLineEdit = QtWidgets.QLineEdit(self.frame)
        self.addressLineEdit.setGeometry(QtCore.QRect(80, 300, 113, 20))
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.addressLineEdit.setReadOnly(True)  # Make read-only

        self.countryLabel = QtWidgets.QLabel(self.frame)
        self.countryLabel.setGeometry(QtCore.QRect(80, 340, 76, 16))
        self.countryLabel.setObjectName("countryLabel")
        self.countryLineEdit = QtWidgets.QLineEdit(self.frame)
        self.countryLineEdit.setGeometry(QtCore.QRect(80, 360, 113, 20))
        self.countryLineEdit.setObjectName("countryLineEdit")
        self.countryLineEdit.setReadOnly(True)  # Make read-only

        self.totalLineEdit = QtWidgets.QLineEdit(self.frame)
        self.totalLineEdit.setGeometry(QtCore.QRect(405, 90, 113, 20))
        self.totalLineEdit.setObjectName("totalLineEdit")
        self.totalLabel = QtWidgets.QLabel(self.frame)
        self.totalLabel.setGeometry(QtCore.QRect(405, 70, 66, 16))
        self.totalLabel.setObjectName("totalLabel")

        self.orderDateEdit = QtWidgets.QDateEdit(self.frame)
        self.orderDateEdit.setGeometry(QtCore.QRect(405, 140, 113, 20))
        self.orderDateEdit.setCalendarPopup(True)
        self.orderDateEdit.setObjectName("orderDateEdit")
        self.orderDateEdit.setDate(QtCore.QDate.currentDate())
        self.orderDateLabel = QtWidgets.QLabel(self.frame)
        self.orderDateLabel.setGeometry(QtCore.QRect(405, 120, 66, 16))
        self.orderDateLabel.setObjectName("orderDateLabel")

        self.prodNameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.prodNameLineEdit.setGeometry(QtCore.QRect(405, 195, 113, 20))
        self.prodNameLineEdit.setObjectName("prodNameLineEdit")
        self.product_Label = QtWidgets.QLabel(self.frame)
        self.product_Label.setGeometry(QtCore.QRect(405, 175, 81, 16))
        self.product_Label.setObjectName("product_Label")

        self.quantityLineEdit = QtWidgets.QLineEdit(self.frame)
        self.quantityLineEdit.setGeometry(QtCore.QRect(405, 300, 113, 20))
        self.quantityLineEdit.setObjectName("quantityLineEdit")
        self.quantityLabel = QtWidgets.QLabel(self.frame)
        self.quantityLabel.setGeometry(QtCore.QRect(405, 280, 86, 16))
        self.quantityLabel.setObjectName("quantityLabel")

        self.rollsizeLabel = QtWidgets.QLabel(self.frame)
        self.rollsizeLabel.setGeometry(QtCore.QRect(405, 340, 47, 14))
        self.rollsizeLabel.setObjectName("rollsizeLabel")
        self.rollsizeLineEdit1 = QtWidgets.QLineEdit(self.frame)
        self.rollsizeLineEdit1.setGeometry(QtCore.QRect(405, 360, 45, 20))
        self.rollsizeLineEdit1.setObjectName("rollsizeLineEdit1")
        self.rollsizeLineEdit2 = QtWidgets.QLineEdit(self.frame)
        self.rollsizeLineEdit2.setGeometry(QtCore.QRect(475, 360, 45, 20))
        self.rollsizeLineEdit2.setObjectName("rollsizeLineEdit2")

        self.label_times = QtWidgets.QLabel(self.frame)
        self.label_times.setGeometry(QtCore.QRect(459, 360, 10, 20))  
        self.label_times.setObjectName("label_times")
        font = QtGui.QFont()
        font.setBold(True) 
        self.label_times.setFont(font)
        self.label_times.setText("X")

        self.thicknessLineEdit = QtWidgets.QLineEdit(self.frame)
        self.thicknessLineEdit.setGeometry(QtCore.QRect(405, 250, 113, 20))
        self.thicknessLineEdit.setObjectName("thicknessLineEdit")
        self.thicknessLabel = QtWidgets.QLabel(self.frame)
        self.thicknessLabel.setGeometry(QtCore.QRect(405, 230, 81, 16))
        self.thicknessLabel.setObjectName("thicknessLabel")

        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.clicked.connect(UpdatePurchase.close)
        self.Cancel.setGeometry(QtCore.QRect(370, 410, 96, 31))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setObjectName("Cancel")
        font_Cancel = QtGui.QFont()
        font_Cancel.setFamily("Arial")
        font_Cancel.setPointSize(9)
        font_Cancel.setBold(True)
        self.Cancel.setFont(font_Cancel)

        self.UpdatePurchase_3 = QtWidgets.QPushButton(self.frame)
        self.UpdatePurchase_3.clicked.connect(self.save_data)
        self.UpdatePurchase_3.setGeometry(QtCore.QRect(480, 410, 120, 31))
        self.UpdatePurchase_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.UpdatePurchase_3.setObjectName("UpdatePurchase_3")
        font_add = QtGui.QFont()
        font_add.setFamily("Arial")
        font_add.setPointSize(9)
        font_add.setBold(True)
        self.UpdatePurchase_3.setFont(font_add)

        self.retranslateUi(UpdatePurchase)
        QtCore.QMetaObject.connectSlotsByName(UpdatePurchase)

        # Set tab order
        UpdatePurchase.setTabOrder(self.searchLineEdit, self.searchButton)
        UpdatePurchase.setTabOrder(self.searchButton, self.lineEdit)
        UpdatePurchase.setTabOrder(self.lineEdit, self.emailLineEdit)
        UpdatePurchase.setTabOrder(self.emailLineEdit, self.contactLineEdit)
        UpdatePurchase.setTabOrder(self.contactLineEdit, self.addressLineEdit)
        UpdatePurchase.setTabOrder(self.addressLineEdit, self.countryLineEdit)
        UpdatePurchase.setTabOrder(self.countryLineEdit, self.totalLineEdit)
        UpdatePurchase.setTabOrder(self.totalLineEdit, self.orderDateEdit)
        UpdatePurchase.setTabOrder(self.orderDateEdit, self.prodNameLineEdit)
        UpdatePurchase.setTabOrder(self.prodNameLineEdit, self.thicknessLineEdit)
        UpdatePurchase.setTabOrder(self.thicknessLineEdit, self.quantityLineEdit)
        UpdatePurchase.setTabOrder(self.quantityLineEdit, self.rollsizeLineEdit1)
        UpdatePurchase.setTabOrder(self.rollsizeLineEdit1, self.rollsizeLineEdit2)
        UpdatePurchase.setTabOrder(self.rollsizeLineEdit2, self.Cancel)
        UpdatePurchase.setTabOrder(self.Cancel, self.UpdatePurchase_3)

    def retranslateUi(self, UpdatePurchase):
        _translate = QtCore.QCoreApplication.translate
        UpdatePurchase.setWindowTitle(_translate("UpdatePurchase", "Update Purchase"))
        self.UpdatePurchase.setText(_translate("UpdatePurchase", "Update Purchase"))
        self.searchLabel.setText(_translate("UpdatePurchase", "Search Supplier ID"))
        self.searchButton.setText(_translate("UpdatePurchase", "Search"))
        self.label.setText(_translate("UpdatePurchase", "Supplier Name"))
        self.emailLabel.setText(_translate("UpdatePurchase", "Email Address"))
        self.contactLabel.setText(_translate("UpdatePurchase", "Contact Number"))
        self.addressLabel.setText(_translate("UpdatePurchase", "Address"))
        self.countryLabel.setText(_translate("UpdatePurchase", "Country"))
        self.totalLabel.setText(_translate("UpdatePurchase", "Total Amount"))
        self.orderDateLabel.setText(_translate("UpdatePurchase", "Ordered Date"))
        self.product_Label.setText(_translate("UpdatePurchase", "Product Name"))
        self.rollsizeLabel.setText(_translate("UpdatePurchase", "Roll Size"))
        self.quantityLabel.setText(_translate("UpdatePurchase", "Quantity"))
        self.thicknessLabel.setText(_translate("UpdatePurchase", "Thickness"))
        self.Cancel.setText(_translate("UpdatePurchase", "Cancel"))
        self.UpdatePurchase_3.setText(_translate("UpdatePurchase", "Update Purchase"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UpdatePurchase = QtWidgets.QDialog()
    ui = Ui_UpdatePurchase(UpdatePurchase)
    ui.setupUi(UpdatePurchase)
    UpdatePurchase.show()
    sys.exit(app.exec_())
