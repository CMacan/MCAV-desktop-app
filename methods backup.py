# Navbar Global

    def show_purchase(self):
        from PurchaseView import Ui_PurchaseView
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_PurchaseView()
        self.ui.setupUi(self.window2)
        self.window2.show()
       
    def order(self):
        from Order import Ui_Order_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Order_2()
        self.ui.setupUi(self.window2)
        self.window2.show()

    def inventory(self):
        from Inventory import Ui_Inventory_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Inventory_2()
        self.ui.setupUi(self.window2)
        self.window2.show()

    def report(self):
        from Report import Ui_Report_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Report_2()
        self.ui.setupUi(self.window2)
        self.window2.show()

    def purchase(self):
        from PurchaseView import Ui_PurchaseView
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_PurchaseView()
        self.ui.setupUi(self.window2)
        self.window2.show()

    def customer(self):
        from Customer import Ui_Customer_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Customer_2()
        self.ui.setupUi(self.window2)
        self.window2.show()

    def profile(self):
        from Profile import Ui_Profile_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Profile_2()
        self.ui.setupUi(self.window2)
        self.window2.show()

    # insert below QPushButton
        self.Inventory.clicked.connect(self.inventory)
        self.Inventory.clicked.connect(Dasboard.close)


    # PostgreSQL connection
    def __init__(self):
        
        self.conn = psycopg2.connect(host="aws-1-ap-northeast-2.pooler.supabase.com", dbname="postgres", 
                                     user="postgres.qtfyvvwktvfviudotoxh", password="isy9KwSEmgbTdbxi", 
                                     port=6543)
        self.cur = self.conn.cursor()



# AddOrder.py

    def save_data(self):
        # Get data from UI elements
        cus_fname = self.lineEdit.text()
        cus_lname = self.lineEdit_5.text()
        cus_email = self.lineEdit_2.text()
        cus_phone = self.lineEdit_3.text()
        cus_address = self.lineEdit_14.text()

        sql = """
        CREATE TABLE IF NOT EXISTS CUSTOMER (
            CUS_FNAME VARCHAR(255),
            CUS_LNAME VARCHAR(255),
            CUS_EMAIL VARCHAR(255),
            CUS_PHONE VARCHAR(20),
            CUS_ADDRESS TEXT
        );

        INSERT INTO CUSTOMER (CUS_FNAME, CUS_LNAME, CUS_EMAIL, CUS_PHONE, CUS_ADDRESS) VALUES (%s, %s, %s, %s, %s)
        """
        self.cur.execute(sql, (cus_fname, cus_lname, cus_email, cus_phone, cus_address))
        
        self.conn.commit()