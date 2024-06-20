from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import psycopg2

class Ui_UpdateOrder(object):
    def __init__(self, order_id):
        # PostgreSQL connection
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", dbname="postgres", user="postgres.oxzprkjuxnjgnfihweyj",
                                     password="Milliondollarbaby123", port=6543)
        self.cur = self.conn.cursor()
        self.order_id = order_id
    
    def save_data(self):
        # Get data from UI elements
        cus_code = self.searchLineEdit.text().strip()
        order_total = self.totalLineEdit.text()
        order_product = self.prodNameLineEdit.text()
        order_quantity = self.quantityLineEdit.text()
        order_date = self.orderDateEdit.date().toString(QtCore.Qt.ISODate)
        order_complete_date = self.orderDateEdit.date().toString(QtCore.Qt.ISODate)
        order_rollsize_width = self.rollsizeLineEdit1.text()
        order_rollsize_height = self.rollsizeLineEdit2.text()
        order_rollsize = (f'{order_rollsize_width} X {order_rollsize_height}')

        # Validate input data
        if not (cus_code and order_total and order_product and order_quantity and order_date):
            self.show_message("Error", "Please fill all the fields.")
            return

        try:
            # Update order details using the stored order ID
            sql_update_order = """
            UPDATE ORDER 
            SET SUP_ID = %s, ORD_AMOUNT = %s, ORD_ORDER_DATE = %s, ORD_PRODUCT_NAME = %s,
            PUR_THICKNESS = %s, ORD_QUANTITY = %s, ORD_ROLL_SIZE = %s
            WHERE ORD_ID = %s
            """

            self.cur.execute(sql_update_order, (cus_code, order_total, order_product, order_quantity, order_date, order_rollsize, self.order_id))
            self.conn.commit()

            self.show_message("Success", "Order updated successfully.")
            
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

    def search_customer(self):
        cus_code = self.searchLineEdit.text().strip()
        if not cus_code:
            self.show_message("Error", "Please enter a Customer ID to search.")
            return

        try:
            self.cur.execute("SELECT CUS_FNAME, CUS_LNAME, CUS_EMAIL, CUS_PHONE, CUS_ADDRESS FROM CUSTOMER WHERE CUS_CODE = %s", (cus_code,))
            customer_data = self.cur.fetchone()
            if customer_data:
                cus_fname, cus_lname, cus_email, cus_contact, cus_address = customer_data
                self.lineEdit.setText(cus_fname)
                self.lnameLineEdit.setText(cus_lname)
                self.emailLineEdit.setText(cus_email)
                self.contactLineEdit.setText(cus_contact)
                self.addressLineEdit.setText(cus_address)
            else:
                self.show_message("Not Found", "Customer ID not found.")
        except psycopg2.Error as e:
            error_message = f"Error fetching data: {e.pgcode} - {e.pgerror}"
            self.show_message("Error", error_message)    


    def setupUi(self, UpdateOrder):
        UpdateOrder.setObjectName("UpdateOrder")
        UpdateOrder.resize(640, 480)
        self.frame = QtWidgets.QFrame(UpdateOrder)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgb(255, 255, 255);
            }
            QLabel#UpdateOrder {
                font-size: 25px;
            }
            QLineEdit {
                width: 200px;
            }
            QLineEdit#lineEdit,                     
            QLineEdit#customerLineEdit, 
            QLineEdit#lnameLineEdit, 
            QLineEdit#emailLineEdit, 
            QLineEdit#contactLineEdit,
            QLineEdit#addressLineEdit {
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
        self.UpdateOrder = QtWidgets.QLabel(self.frame)
        self.UpdateOrder.setGeometry(QtCore.QRect(35, 20, 250, 50))
        self.UpdateOrder.setObjectName("UpdateOrder")
        font_UpdateOrder = QtGui.QFont()
        font_UpdateOrder.setFamily("Arial")
        font_UpdateOrder.setPointSize(15)
        font_UpdateOrder.setBold(True)
        self.UpdateOrder.setFont(font_UpdateOrder)

        self.searchLineEdit = QtWidgets.QLineEdit(self.frame)
        self.searchLineEdit.setGeometry(QtCore.QRect(80, 90, 111, 20))
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.searchLabel = QtWidgets.QLabel(self.frame)
        self.searchLabel.setGeometry(QtCore.QRect(80, 70, 111, 16))
        self.searchLabel.setObjectName("searchLabel")

        self.searchButton = QtWidgets.QPushButton(self.frame)
        self.searchButton.setGeometry(QtCore.QRect(200, 90, 75, 23))
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchButton.setObjectName("searchButton")
        font_search = QtGui.QFont()
        font_search.setFamily("Arial")
        font_search.setPointSize(8)
        font_search.setBold(True)
        self.searchButton.setFont(font_search)
        self.searchButton.clicked.connect(self.search_customer) 

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, 120, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 140, 111, 20))
        self.lineEdit.setMaxLength(300)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)  

        self.lnameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.lnameLineEdit.setGeometry(QtCore.QRect(80, 195, 113, 20))
        self.lnameLineEdit.setObjectName("lnameLineEdit")
        self.lnameLineEdit.setReadOnly(True)  
        self.lnameLabel = QtWidgets.QLabel(self.frame)
        self.lnameLabel.setGeometry(QtCore.QRect(80, 175, 76, 16))
        self.lnameLabel.setObjectName("lnameLabel")

        self.emailLineEdit = QtWidgets.QLineEdit(self.frame)
        self.emailLineEdit.setGeometry(QtCore.QRect(80, 250, 113, 20))
        self.emailLineEdit.setObjectName("emailLineEdit")
        self.emailLineEdit.setReadOnly(True)  # Make read-only
        self.emailLabel = QtWidgets.QLabel(self.frame)
        self.emailLabel.setGeometry(QtCore.QRect(80, 230, 81, 16))
        self.emailLabel.setObjectName("emailLabel")

        self.contactLabel = QtWidgets.QLabel(self.frame)
        self.contactLabel.setGeometry(QtCore.QRect(80, 280, 76, 16))
        self.contactLabel.setObjectName("contactLabel")
        self.contactLineEdit = QtWidgets.QLineEdit(self.frame)
        self.contactLineEdit.setGeometry(QtCore.QRect(80, 300, 113, 20))
        self.contactLineEdit.setObjectName("contactLineEdit")
        self.contactLineEdit.setReadOnly(True)  # Make read-only

        self.addressLabel = QtWidgets.QLabel(self.frame)
        self.addressLabel.setGeometry(QtCore.QRect(80, 340, 76, 16))
        self.addressLabel.setObjectName("addressLabel")
        self.addressLineEdit = QtWidgets.QLineEdit(self.frame)
        self.addressLineEdit.setGeometry(QtCore.QRect(80, 360, 113, 20))
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.addressLineEdit.setReadOnly(True)  # Make read-only

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

        self.categoryLineEdit = QtWidgets.QLineEdit(self.frame)
        self.categoryLineEdit.setGeometry(QtCore.QRect(405, 250, 113, 20))
        self.categoryLineEdit.setObjectName("categoryLineEdit")
        self.categoryLabel = QtWidgets.QLabel(self.frame)
        self.categoryLabel.setGeometry(QtCore.QRect(405, 230, 81, 16))
        self.categoryLabel.setObjectName("categoryLabel")

        self.Cancel = QtWidgets.QPushButton(self.frame)
        self.Cancel.clicked.connect(UpdateOrder.close)
        self.Cancel.setGeometry(QtCore.QRect(370, 410, 96, 31))
        self.Cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cancel.setObjectName("Cancel")
        font_Cancel = QtGui.QFont()
        font_Cancel.setFamily("Arial")
        font_Cancel.setPointSize(9)
        font_Cancel.setBold(True)
        self.Cancel.setFont(font_Cancel)

        self.UpdateOrder_3 = QtWidgets.QPushButton(self.frame)
        self.UpdateOrder_3.clicked.connect(self.save_data)
        self.UpdateOrder_3.setGeometry(QtCore.QRect(480, 410, 120, 31))
        self.UpdateOrder_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.UpdateOrder_3.setObjectName("UpdateOrder_3")
        font_add = QtGui.QFont()
        font_add.setFamily("Arial")
        font_add.setPointSize(9)
        font_add.setBold(True)
        self.UpdateOrder_3.setFont(font_add)

        self.retranslateUi(UpdateOrder)
        QtCore.QMetaObject.connectSlotsByName(UpdateOrder)

        # Set tab order
        UpdateOrder.setTabOrder(self.searchLineEdit, self.searchButton)
        UpdateOrder.setTabOrder(self.searchButton, self.lineEdit)
        UpdateOrder.setTabOrder(self.lineEdit, self.lnameLineEdit)
        UpdateOrder.setTabOrder(self.lnameLineEdit, self.emailLineEdit)
        UpdateOrder.setTabOrder(self.emailLineEdit, self.contactLineEdit)
        UpdateOrder.setTabOrder(self.contactLineEdit, self.addressLineEdit)
        UpdateOrder.setTabOrder(self.addressLineEdit, self.totalLineEdit)
        UpdateOrder.setTabOrder(self.totalLineEdit, self.orderDateEdit)
        UpdateOrder.setTabOrder(self.orderDateEdit, self.prodNameLineEdit)
        UpdateOrder.setTabOrder(self.prodNameLineEdit, self.categoryLineEdit)
        UpdateOrder.setTabOrder(self.categoryLineEdit, self.quantityLineEdit)
        UpdateOrder.setTabOrder(self.quantityLineEdit, self.rollsizeLineEdit1)
        UpdateOrder.setTabOrder(self.rollsizeLineEdit1, self.rollsizeLineEdit2)
        UpdateOrder.setTabOrder(self.rollsizeLineEdit2, self.Cancel)
        UpdateOrder.setTabOrder(self.Cancel, self.UpdateOrder_3)

    def retranslateUi(self, UpdateOrder):
        _translate = QtCore.QCoreApplication.translate
        UpdateOrder.setWindowTitle(_translate("UpdateOrder", "Update Order"))
        self.UpdateOrder.setText(_translate("UpdateOrder", "Update Order"))
        self.searchLabel.setText(_translate("UpdateOrder", "Search Customer ID"))
        self.searchButton.setText(_translate("UpdateOrder", "Search"))
        self.label.setText(_translate("UpdateOrder", "Customer First Name"))
        self.lnameLabel.setText(_translate("UpdateOrder", "Customer Last Name"))
        self.emailLabel.setText(_translate("UpdateOrder", "Email Address"))
        self.contactLabel.setText(_translate("UpdateOrder", "Contact Number"))
        self.addressLabel.setText(_translate("UpdateOrder", "Address"))
        self.totalLabel.setText(_translate("UpdateOrder", "Total Amount"))
        self.orderDateLabel.setText(_translate("UpdateOrder", "Ordered Date"))
        self.product_Label.setText(_translate("UpdateOrder", "Product Name"))
        self.rollsizeLabel.setText(_translate("UpdateOrder", "Roll Size"))
        self.quantityLabel.setText(_translate("UpdateOrder", "Quantity"))
        self.categoryLabel.setText(_translate("UpdateOrder", "Category"))
        self.Cancel.setText(_translate("UpdateOrder", "Cancel"))
        self.UpdateOrder_3.setText(_translate("UpdateOrder", "Update Order"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UpdateOrder = QtWidgets.QDialog()
    ui = Ui_UpdateOrder(UpdateOrder)
    ui.setupUi(UpdateOrder)
    UpdateOrder.show()
    sys.exit(app.exec_())
