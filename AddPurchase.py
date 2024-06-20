import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,  QDialogButtonBox
import datetime

class Ui_AddPurchase(object):

    def __init__(self):
        # PostgreSQL connection
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", dbname="postgres", user="postgres.oxzprkjuxnjgnfihweyj",
                                     password="Milliondollarbaby123", port=6543)
        self.cur = self.conn.cursor()

    def save_data(self):
        # Get data from UI elements
        sup_id = self.searchLineEdit.text().strip()
        pur_total = self.totalLineEdit.text().strip()
        pur_order_date = self.orderDateEdit.date().toString(QtCore.Qt.ISODate)
        pur_product_name = self.prodNameLineEdit.text().strip()
        pur_quantity = self.quantityLineEdit.text().strip()
        pur_thickness = self.thicknessLineEdit.text().strip()
        rollsize_width = self.rollsizeLineEdit1.text().strip()
        rollsize_length = self.rollsizeLineEdit2.text().strip()

        pur_roll_size = f"{rollsize_width} x {rollsize_length}"

        # Validate input data
        if not all([sup_id, pur_order_date, pur_product_name, pur_quantity]):
            missing_fields = []
            if not sup_id:
                missing_fields.append("Supplier ID")
            if not pur_total:
                missing_fields.append("Total Amount")
            if not pur_order_date:
                missing_fields.append("Order Date")
            if not pur_product_name:
                missing_fields.append("Product Name")
            if not pur_quantity:
                missing_fields.append("Quantity")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Please input all required fields:\n{', '.join(missing_fields)}")
            msg.setWindowTitle("Required Fields")
            msg.exec_()
            return

        confirm_msg = QMessageBox()
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setText("Add to Purchase list?")
        confirm_msg.setWindowTitle("Confirmation")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        result = confirm_msg.exec_()

        if result == QMessageBox.Yes:
            # Insert into SUPPLIER table
            try:
                # Insert into PURCHASE table
                sql_purchase = """
                INSERT INTO PURCHASE (SUP_ID, PUR_AMOUNT, PUR_ORDER_DATE, PUR_PRODUCT_NAME, PUR_QUANTITY, PUR_THICKNESS, PUR_ROLL_SIZE)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

                self.cur.execute(sql_purchase, (sup_id, pur_total, pur_order_date, pur_product_name, pur_quantity, pur_thickness, pur_roll_size))
                self.conn.commit()
                self.show_message("Success", "Data saved successfully.")
                self.clear_input_fields()
                self.set_current_date()

            except psycopg2.Error as e:
                self.conn.rollback()  # Roll back transaction on error
                error_message = f"Error saving data: {e.pgcode} - {e.pgerror}"
                self.show_message("Error", error_message)

    def clear_input_fields(self):
        self.searchLineEdit.clear()
        self.lineEdit.clear()
        self.quantityLineEdit.clear()
        self.emailLineEdit.clear()
        self.contactLineEdit.clear()
        self.addressLineEdit.clear()
        self.countryLineEdit.clear()
        self.totalLineEdit.clear()
        self.totalLineEdit.clear()
        self.addressLineEdit.clear()
        self.orderDateEdit.setDate(QtCore.QDate())
        self.prodNameLineEdit.clear()
        self.thicknessLineEdit.clear()
        self.quantityLineEdit.clear()
        self.rollsizeLineEdit1.clear()
        self.rollsizeLineEdit2.clear()  

    def set_current_date(self):
        current_date = datetime.date.today()
        qt_date = QtCore.QDate(current_date.year, current_date.month, current_date.day)
        self.orderDateEdit.setDate(qt_date)

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

    def setupUi(self, AddPurchase):
        AddPurchase.setObjectName("AddPurchase")
        AddPurchase.resize(640, 480)
        self.frame = QtWidgets.QFrame(AddPurchase)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgb(255, 255, 255);
            }
            QLabel#AddOrder {
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
        self.AddOrder = QtWidgets.QLabel(self.frame)
        self.AddOrder.setGeometry(QtCore.QRect(35, 30, 161, 26))
        self.AddOrder.setObjectName("AddOrder")

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
        self.Cancel.clicked.connect(AddPurchase.close)
        self.Cancel.setGeometry(QtCore.QRect(370, 410, 96, 31))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setObjectName("Cancel")
        font_Cancel = QtGui.QFont()
        font_Cancel.setFamily("Arial")
        font_Cancel.setPointSize(9)
        font_Cancel.setBold(True)
        self.Cancel.setFont(font_Cancel)

        self.AddOrder_3 = QtWidgets.QPushButton(self.frame)
        self.AddOrder_3.clicked.connect(self.save_data)
        self.AddOrder_3.setGeometry(QtCore.QRect(480, 410, 100, 31))
        self.AddOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddOrder_3.setObjectName("AddOrder_3")
        font_add = QtGui.QFont()
        font_add.setFamily("Arial")
        font_add.setPointSize(9)
        font_add.setBold(True)
        self.AddOrder_3.setFont(font_add)

        self.retranslateUi(AddPurchase)
        QtCore.QMetaObject.connectSlotsByName(AddPurchase)

        # Set tab order
        AddPurchase.setTabOrder(self.searchLineEdit, self.searchButton)
        AddPurchase.setTabOrder(self.searchButton, self.lineEdit)
        AddPurchase.setTabOrder(self.lineEdit, self.emailLineEdit)
        AddPurchase.setTabOrder(self.emailLineEdit, self.contactLineEdit)
        AddPurchase.setTabOrder(self.contactLineEdit, self.addressLineEdit)
        AddPurchase.setTabOrder(self.addressLineEdit, self.countryLineEdit)
        AddPurchase.setTabOrder(self.countryLineEdit, self.totalLineEdit)
        AddPurchase.setTabOrder(self.totalLineEdit, self.orderDateEdit)
        AddPurchase.setTabOrder(self.orderDateEdit, self.prodNameLineEdit)
        AddPurchase.setTabOrder(self.prodNameLineEdit, self.thicknessLineEdit)
        AddPurchase.setTabOrder(self.thicknessLineEdit, self.quantityLineEdit)
        AddPurchase.setTabOrder(self.quantityLineEdit, self.rollsizeLineEdit1)
        AddPurchase.setTabOrder(self.rollsizeLineEdit1, self.rollsizeLineEdit2)
        AddPurchase.setTabOrder(self.rollsizeLineEdit2, self.Cancel)
        AddPurchase.setTabOrder(self.Cancel, self.AddOrder_3)

    def retranslateUi(self, AddPurchase):
        _translate = QtCore.QCoreApplication.translate
        AddPurchase.setWindowTitle(_translate("AddPurchase", "Add Purchase"))
        self.AddOrder.setText(_translate("AddPurchase", "Add Purchase"))
        self.searchLabel.setText(_translate("AddPurchase", "Search Supplier ID"))
        self.searchButton.setText(_translate("AddPurchase", "Search"))
        self.label.setText(_translate("AddPurchase", "Supplier Name"))
        self.emailLabel.setText(_translate("AddPurchase", "Email Address"))
        self.contactLabel.setText(_translate("AddPurchase", "Contact Number"))
        self.addressLabel.setText(_translate("AddPurchase", "Address"))
        self.countryLabel.setText(_translate("AddPurchase", "Country"))
        self.totalLabel.setText(_translate("AddPurchase", "Total Amount"))
        self.orderDateLabel.setText(_translate("AddPurchase", "Ordered Date"))
        self.product_Label.setText(_translate("AddPurchase", "Product Name"))
        self.rollsizeLabel.setText(_translate("AddPurchase", "Roll Size"))
        self.quantityLabel.setText(_translate("AddPurchase", "Quantity"))
        self.thicknessLabel.setText(_translate("AddPurchase", "Thickness"))
        self.Cancel.setText(_translate("AddPurchase", "Cancel"))
        self.AddOrder_3.setText(_translate("AddPurchase", "Add Purchase"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddPurchase = QtWidgets.QDialog()
    ui = Ui_AddPurchase()
    ui.setupUi(AddPurchase)
    AddPurchase.show()
    sys.exit(app.exec_())
