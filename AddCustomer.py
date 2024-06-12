import sys
from PyQt5 import QtWidgets, uic
import psycopg2

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('AddCustomerPopUpWindow.ui', self)  # Load the UI file

        # Connect button click event to a function
        self.AddOrderButton_3.clicked.connect(self.save_data)

        # PostgreSQL connection
        self.conn = psycopg2.connect(host="localhost", dbname="MCAV", user="postgres", 
                                     password="1234", port=5432)
        self.cur = self.conn.cursor()

    def save_data(self):
        # Get data from UI elements
        cus_fname = self.cus_fname_lineEdit.text()
        cus_lname = self.cus_lname_lineEdit.text()
        cus_email = self.cus_email_lineEdit.text()
        cus_phone = self.cus_phone_lineEdit.text()
        cus_address = self.cus_address_lineEdit.text()

        sql = "INSERT INTO CUSTOMER (CUS_FNAME, CUS_LNAME, CUS_EMAIL, CUS_PHONE, CUS_ADDRESS) VALUES (%s, %s, %s, %s, %s)"
        self.cur.execute(sql, (cus_fname, cus_lname, cus_email, cus_phone, cus_address))
        
        self.conn.commit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
