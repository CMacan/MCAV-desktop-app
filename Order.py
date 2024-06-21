from PyQt5 import QtCore, QtGui, QtWidgets
from clickable import ClickableLabel 
import psycopg2
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QDate
class Ui_Order_2(object):

    def __init__(self):
        # PostgreSQL connection
        self.conn = psycopg2.connect(host="aws-0-ap-southeast-1.pooler.supabase.com", dbname="postgres", user="postgres.oxzprkjuxnjgnfihweyj", 
                                     password="Milliondollarbaby123", port=6543)
        self.cur = self.conn.cursor()
        

    def fetch_orders_with_details(self):
        try:
            query = """
            SELECT ORDERS.ORD_ID, CUSTOMER.CUS_CODE, PRODUCT.PROD_CATEGORY, PRODUCT.PROD_NAME, ORDERS.ORD_SIZE, 
                ORDERS.ORD_QUANTITY, ORDERS.ORD_TOTAL_AMOUNT, ORDERS.ORD_DATE, ORDERS.ORD_DATE_COMPLETION
            FROM ORDERS
            JOIN CUSTOMER ON ORDERS.CUS_CODE = CUSTOMER.CUS_CODE
            JOIN PRODUCT ON ORDERS.PROD_ID = PRODUCT.PROD_ID
            """
            self.cur.execute(query)
            return self.cur.fetchall()
        except psycopg2.Error as e:
            self.show_message("Database Error", f"Error fetching data from database: {e}")
            return []

    def show_message(self, title, message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def search(self):
        search_text = self.SearchInput.text().strip()
        
        if not search_text:
            try:
                # Fetch all products from the PRODUCT table
                sql_all_order = """
                SELECT ORDERS.ORD_ID, CUSTOMER.CUS_CODE, PRODUCT.PROD_CATEGORY, PRODUCT.PROD_NAME, ORDERS.ORD_SIZE, 
                ORDERS.ORD_QUANTITY, ORDERS.ORD_TOTAL_AMOUNT, ORDERS.ORD_DATE, ORDERS.ORD_DATE_COMPLETION
                FROM ORDERS
                JOIN CUSTOMER ON ORDERS.CUS_CODE = CUSTOMER.CUS_CODE
                JOIN PRODUCT ON ORDERS.PROD_ID = PRODUCT.PROD_ID
                """
                self.cur.execute(sql_all_order)
                results = self.cur.fetchall()
                self.display_orders(results)
            except psycopg2.Error as e:
                self.show_message("Database Error", f"Error fetching orders: {e}")
            
            return

        try:
            sql_search = """
            SELECT ORDERS.ORD_ID, CUSTOMER.CUS_CODE, PRODUCT.PROD_CATEGORY, PRODUCT.PROD_NAME, ORDERS.ORD_SIZE, 
            ORDERS.ORD_QUANTITY, ORDERS.ORD_TOTAL_AMOUNT, ORDERS.ORD_DATE, ORDERS.ORD_DATE_COMPLETION
            FROM ORDERS
            JOIN CUSTOMER ON ORDERS.CUS_CODE = CUSTOMER.CUS_CODE
            JOIN PRODUCT ON ORDERS.PROD_ID = PRODUCT.PROD_ID
            WHERE PROD_CATEGORY ILIKE %s
            """
            # Use search_pattern in execute instead of search_text
            search_pattern = f"%{search_text}%"
            self.cur.execute(sql_search, (search_pattern,))
            results = self.cur.fetchall()
            self.display_orders(results)
        except psycopg2.Error as e:
            self.show_message("Database Error", f"Error fetching search results: {e}")

    def display_orders(self, orders):
        self.tableWidget.setRowCount(len(orders))
        self.tableWidget.setRowCount(len(orders))
        self.tableWidget.setColumnCount(10)  # Ensure you have the correct number of columns
        headers = ['Ord_ID', 'Cus_Code', 'Prod_Category', 'Prod_Name', 'Ord_Size', 'Ord_Quantity', 
                   'Ord_total_Amount', 'Ord_date', 'Ord_Date_Completion', 'Actions']
        self.tableWidget.setHorizontalHeaderLabels(headers)
        
        for row_number, order in enumerate(orders):
            for column_number, data in enumerate(order):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText(str(data))
                self.tableWidget.setItem(row_number, column_number, item)

            # Create a widget to hold both edit and delete buttons
            button_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(button_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)  # Adjust spacing between buttons if needed

            edit_button = QtWidgets.QPushButton('Edit')
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50; /* Green */
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            edit_button.clicked.connect(lambda checked, row=row_number: self.update_order(row))
            layout.addWidget(edit_button)

            delete_button = QtWidgets.QPushButton('Delete')
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336; /* Red */
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            delete_button.clicked.connect(lambda checked, row=row_number: self.delete_order(row))
            layout.addWidget(delete_button)

            # Set the widget containing the buttons into the table cell
            cell_widget = QtWidgets.QWidget()
            cell_widget.setLayout(layout)
            self.tableWidget.setCellWidget(row_number, 9, cell_widget)  # Place in the last column

    def delete_order(self, row):
        # Implement delete logic here
        order_id = self.tableWidget.item(row, 0).text()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle('Confirmation')
        msgBox.setText(f"Are you sure you want to delete product?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)

        yes_button = msgBox.button(QtWidgets.QMessageBox.Yes)
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                color: white;
                padding: 5px 10px;
                border: 2px solid #4CAF50; /* Green border */
                border-radius: 5px;
                min-width: 30px;
                min-height: 15px;                 
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Darker Green on hover */
            }
        """)
        
        no_button = msgBox.button(QtWidgets.QMessageBox.No)
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; /* Red */
                color: white;
                padding: 5px 10px;
                border: 2px solid #f44336; /* Red border */
                border-radius: 5px;
                min-width: 30px;
                min-height: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #d32f2f; /* Darker Red on hover */
            }
        """)

        reply = msgBox.exec_()

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                sql = 'DELETE FROM ORDERS WHERE ORD_ID = %s'
                self.cur.execute(sql, (order_id,))
                self.conn.commit()
                QtWidgets.QMessageBox.information(None, 'Success', 'Product deleted successfully!')
                # Refresh table after deletion
                orders = self.fetch_orders_with_details()
                self.display_orders(orders)
            except psycopg2.Error as e:
                QtWidgets.QMessageBox.warning(None, 'Error', f'Database error: {e}')
        else:
            pass
        
    def update_order(self, row):
        from UpdateOrder import Ui_UpdateOrder
        
        # Get data from the selected row
        order_data = []
        for column_number in range(9):  
            item = self.tableWidget.item(row, column_number)
            if item is not None:
                order_data.append(item.text())
            else:
                order_data.append("")

        # Retrieve the order ID from the database
        order_id = order_data[0]  
        sql_get_order_id = "SELECT ORD_ID FROM ORDERS WHERE ORD_ID = %s"
        self.cur.execute(sql_get_order_id, (order_id,))
        order_id_result = self.cur.fetchone()

        if order_id_result is None:
            self.show_message("Error", "Selected order does not exist.")
            return

        order_id = order_id_result[0]
        cus_code = order_data[1]

        # Open the UpdateOrder dialog window
        self.dialog = QDialog()
        self.update_order_ui = Ui_UpdateOrder(order_id)
        self.update_order_ui.setupUi(self.dialog)

        # Populate the QLineEdit fields with data from the database
        self.update_order_ui.searchLineEdit.setText(cus_code)   
        self.update_order_ui.totalLineEdit.setText(order_data[6])   
        self.update_order_ui.orderDateEdit.setDate(QDate.fromString(order_data[8], "yyyy-MM-dd")) 
        self.update_order_ui.comboBox_product.setCurrentText(order_data[3])  
        self.update_order_ui.comboBox.setCurrentText(order_data[2])
        self.update_order_ui.quantityLineEdit.setText(order_data[5]) 

        product_rollsize = order_data[4]

        if product_rollsize:
            dimensions = product_rollsize.split('x') if 'x' in product_rollsize else product_rollsize.split('X')

            # Trim any leading or trailing spaces from each dimension
            dimension1 = dimensions[0].strip()
            dimension2 = dimensions[1].strip()
            self.update_order_ui.rollsizeLineEdit1.setText(dimension1) 
            self.update_order_ui.rollsizeLineEdit2.setText(dimension2)

        self.dialog.exec_()


    def back_dashboard(self):
        from Dashboard import Ui_Dasboard
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Dasboard()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()
    
    def add_new_order(self):
        from AddOrder  import Ui_AddOrder
        self.window2 = QtWidgets.QDialog()
        self.ui = Ui_AddOrder()
        self.ui.setupUi(self.window2)
        self.window2.setModal(True)
        self.window2.exec_() 
        
    def order(self):
        from Order import Ui_Order_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Order_2()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()

    def inventory(self):
        from Inventory import Ui_Inventory_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Inventory_2()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()


    def order(self):
        from Order import Ui_Order_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Order_2()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()

    def purchase(self):
        from PurchaseView import Ui_PurchaseView
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_PurchaseView()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()

    def customer(self):
        from Customer import Ui_Customer_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Customer_2()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()

    def profile(self):
        from Profile import Ui_Profile_2
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Profile_2()
        self.ui.setupUi(self.window2)
        self.window2.showMaximized()

    def setupUi(self, Order_2):
        Order_2.setObjectName("Order_2")
        Order_2.resize(998, 491)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Order_2.sizePolicy().hasHeightForWidth())
        Order_2.setSizePolicy(sizePolicy)
        Order_2.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(Order_2)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.NavbarFrame = QtWidgets.QFrame(self.centralwidget)
        self.NavbarFrame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NavbarFrame.sizePolicy().hasHeightForWidth())
        self.NavbarFrame.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NavbarFrame.setFont(font)
        self.NavbarFrame.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.NavbarFrame.setStyleSheet("QPushButton {\n"
"    min-width: 100px; \n"
"    max-width: 150px;\n"
"    min-height: 40px;\n"
"    max-height: 35px;\n"
"    font-size:12px;\n"
"    border: 2px solid #8f8f91; \n"
"    border-radius: 10px;\n"
"    background-color: #d8d8d8; \n"
"    min-width: 80px; \n"
"    min-height: 30px; \n"
"    padding: 5px; \n"
"    color: black; \n"
"    font-weight: bold; \n"
"}\n"
"")
        self.NavbarFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.NavbarFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.NavbarFrame.setObjectName("NavbarFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.NavbarFrame)
        self.horizontalLayout.setContentsMargins(5, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Logo = QtWidgets.QLabel(self.NavbarFrame)
        self.Logo.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Logo.sizePolicy().hasHeightForWidth())
        self.Logo.setSizePolicy(sizePolicy)
        self.Logo.setMinimumSize(QtCore.QSize(55, 55))
        self.Logo.setMaximumSize(QtCore.QSize(55, 55))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Logo.setFont(font)
        self.Logo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Logo.setAutoFillBackground(False)
        self.Logo.setStyleSheet("")
        self.Logo.setText("")
        self.Logo.setTextFormat(QtCore.Qt.RichText)
        self.Logo.setPixmap(QtGui.QPixmap("static/logo.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setWordWrap(False)
        self.Logo.setObjectName("Logo")
        self.horizontalLayout.addWidget(self.Logo)
        self.tarp = ClickableLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.tarp.setFont(font)
        self.tarp.setAutoFillBackground(False)
        self.tarp.setStyleSheet("font: 75 12pt 'Georgia';\n"
                                "color: #CD2E2E;")
        self.tarp.setObjectName("tarp")
        self.horizontalLayout.addWidget(self.tarp)
        self.tarp.clicked.connect(self.back_dashboard)
        self.tarp.clicked.connect(Order_2.close)
        self.Inventory = QtWidgets.QPushButton(self.NavbarFrame)
        self.Inventory.clicked.connect(self.inventory)
        self.Inventory.clicked.connect(Order_2.close)
        self.Inventory.setMinimumSize(QtCore.QSize(94, 44))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.Inventory.setFont(font)
        self.Inventory.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Inventory.setStyleSheet("font-size:12px;\n"
"\n"
"")
        self.Inventory.setObjectName("Inventory")
        self.horizontalLayout.addWidget(self.Inventory)
        self.Order = QtWidgets.QPushButton(self.NavbarFrame)
        self.Order.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Order.setStyleSheet("font-size:12px;")
        self.Order.setObjectName("Order")
        self.Order.clicked.connect(self.order)
        self.Order.clicked.connect(Order_2.close)
        self.Order.setStyleSheet("font-size:12px;\n"
        "color: white;\n"
        "border: 2px solid #CD2E2E;\n"
        "background-color: #CD2E2E;\n"
        "")
        self.horizontalLayout.addWidget(self.Order)
        self.Purchase = QtWidgets.QPushButton(self.NavbarFrame)
        self.Purchase.clicked.connect(self.purchase)
        self.Purchase.clicked.connect(Order_2.close)
        self.Purchase.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Purchase.setStyleSheet("font-size:12px;")
        self.Purchase.setObjectName("Purchase")
        self.horizontalLayout.addWidget(self.Purchase)
        self.Customer = QtWidgets.QPushButton(self.NavbarFrame)
        self.Customer.clicked.connect(self.customer)
        self.Customer.clicked.connect(Order_2.close)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.Customer.setFont(font)
        self.Customer.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Customer.setStyleSheet("font-size:12px;")
        self.Customer.setObjectName("Customer")
        self.horizontalLayout.addWidget(self.Customer)
        self.Profile = QtWidgets.QPushButton(self.NavbarFrame)
        self.Profile.clicked.connect(self.profile)
        self.Profile.clicked.connect(Order_2.close)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.Profile.setFont(font)
        self.Profile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Profile.setStyleSheet("font-size:12px;")
        self.Profile.setObjectName("Profile")
        self.horizontalLayout.addWidget(self.Profile)
        self.verticalLayout.addWidget(self.NavbarFrame)
        self.TableContainer = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TableContainer.sizePolicy().hasHeightForWidth())
        self.TableContainer.setSizePolicy(sizePolicy)
        self.TableContainer.setMinimumSize(QtCore.QSize(0, 2))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TableContainer.setFont(font)
        self.TableContainer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TableContainer.setAutoFillBackground(False)
        self.TableContainer.setStyleSheet("background-color: #FAFAFA;\n"
"width: 100vw;")
        self.TableContainer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TableContainer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TableContainer.setObjectName("TableContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.TableContainer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Label = QtWidgets.QFrame(self.TableContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label.sizePolicy().hasHeightForWidth())
        self.Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Label.setFont(font)
        self.Label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Label.setObjectName("Label")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.Label)
        self.horizontalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ProductList = QtWidgets.QFrame(self.Label)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ProductList.setFont(font)
        self.ProductList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ProductList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ProductList.setObjectName("ProductList")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.ProductList)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ProductLabel = QtWidgets.QLabel(self.ProductList)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.ProductLabel.setFont(font)
        self.ProductLabel.setStyleSheet("font-weight: bold;")
        self.ProductLabel.setObjectName("ProductLabel")
        self.verticalLayout_3.addWidget(self.ProductLabel)
        self.manageLabel = QtWidgets.QLabel(self.ProductList)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.manageLabel.setFont(font)
        self.manageLabel.setObjectName("manageLabel")
        self.verticalLayout_3.addWidget(self.manageLabel)
        self.horizontalLayout_4.addWidget(self.ProductList)
        self.BtnContainer = QtWidgets.QFrame(self.Label)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.BtnContainer.setFont(font)
        self.BtnContainer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.BtnContainer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BtnContainer.setObjectName("BtnContainer")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.BtnContainer)
        self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(649, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.AddProduct = QtWidgets.QPushButton(self.BtnContainer)
        self.AddProduct.clicked.connect(self.add_new_order)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddProduct.sizePolicy().hasHeightForWidth())
        self.AddProduct.setSizePolicy(sizePolicy)
        self.AddProduct.setMinimumSize(QtCore.QSize(150, 34))
        self.AddProduct.setMaximumSize(QtCore.QSize(150, 34))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.AddProduct.setFont(font)
        self.AddProduct.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddProduct.setStyleSheet("font-size:12px;\n"
"border: 2px solid #E08028; \n"
"border-radius: 10px;\n"
"background-color: #E08028; \n"
"padding: 5px; \n"
"color: white; \n"
"font-weight: bold; frf")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("static/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddProduct.setIcon(icon)
        self.AddProduct.setIconSize(QtCore.QSize(20, 20))
        self.AddProduct.setObjectName("AddProduct")
        self.horizontalLayout_3.addWidget(self.AddProduct)
        self.horizontalLayout_4.addWidget(self.BtnContainer)
        self.verticalLayout_2.addWidget(self.Label)
        self.DataFrame = QtWidgets.QFrame(self.TableContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DataFrame.sizePolicy().hasHeightForWidth())
        self.DataFrame.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DataFrame.setFont(font)
        self.DataFrame.setStyleSheet("background-color: white;")
        self.DataFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.DataFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DataFrame.setObjectName("DataFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.DataFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.SearchFrame = QtWidgets.QFrame(self.DataFrame)
        self.SearchFrame.setMinimumSize(QtCore.QSize(0, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SearchFrame.setFont(font)
        self.SearchFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.SearchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SearchFrame.setObjectName("SearchFrame")
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.SearchFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.Search = QtWidgets.QLabel(self.SearchFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Search.setFont(font)
        self.Search.setStyleSheet("font-weight: bold;")
        self.Search.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Search.setObjectName("Search")
        self.horizontalLayout_2.addWidget(self.Search)

        self.SearchInput = QtWidgets.QLineEdit(self.SearchFrame)
        self.SearchInput.setMinimumSize(QtCore.QSize(0, 25))
        self.SearchInput.setMaximumSize(QtCore.QSize(200, 25))
        self.SearchInput.setStyleSheet("""
            background-color: #D9D9D9; 
            border-radius: 5px;
            padding-left: 7px; 
            font-size: 10.5pt; 
        """)
        self.SearchInput.setPlaceholderText("Enter Order ID...")
        self.SearchInput.setObjectName("SearchInput")
        self.SearchInput.setFixedWidth(220)
        self.horizontalLayout_2.addWidget(self.SearchInput)

        self.SearchBtn = QtWidgets.QPushButton(self.SearchFrame)
        self.SearchBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SearchBtn.setText("Search")
        self.SearchBtn.setObjectName("SearchBtn")
        self.SearchBtn.setStyleSheet("""
            QPushButton {
                background-color: #E08028; 
                color: white; /* White text color */
                border-radius: 5px; 
                padding: 8px 16px; 
                border: none; 
                font-weight: bold;
                width: 40px;
                height:10px;
            }
            QPushButton:hover {
                background-color: #ff8617; 
            }
        """)

        self.SearchBtn.clicked.connect(self.search)
        self.horizontalLayout_2.addWidget(self.SearchBtn)
        self.verticalLayout_4.addWidget(self.SearchFrame)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)

        self.tableWidget = QtWidgets.QTableWidget(self.DataFrame)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(71, 71, 71))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.tableWidget.setColumnCount(10)
        # Set specific column widths
        self.tableWidget.setColumnWidth(0, 80)  
        self.tableWidget.setColumnWidth(1, 100) 
        self.tableWidget.setColumnWidth(2, 150) 
        self.tableWidget.setColumnWidth(3, 100) 
        self.tableWidget.setColumnWidth(4, 100)  
        self.tableWidget.setColumnWidth(5, 100)  
        self.tableWidget.setColumnWidth(6, 100) 
        self.tableWidget.setColumnWidth(7, 150)  
        self.tableWidget.setColumnWidth(8, 150)  
        self.tableWidget.setColumnWidth(9, 20)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_4.addWidget(self.tableWidget)
        self.verticalLayout_2.addWidget(self.DataFrame)
        self.verticalLayout.addWidget(self.TableContainer)
        Order_2.setCentralWidget(self.centralwidget)

        orders = self.fetch_orders_with_details()
        self.display_orders(orders)

        self.retranslateUi(Order_2)
        QtCore.QMetaObject.connectSlotsByName(Order_2)

    def retranslateUi(self, Order_2):
        _translate = QtCore.QCoreApplication.translate
        Order_2.setWindowTitle(_translate("Order_2", "MainWindow"))
        self.tarp.setText(_translate("Order_2", "TARPAULIN PRINTING SERVICES"))
        self.Inventory.setText(_translate("Order_2", "Inventory"))
        self.Order.setText(_translate("Order_2", "Orders"))
        self.Purchase.setText(_translate("Order_2", "Purchases"))
        self.Customer.setText(_translate("Order_2", "Customers"))
        self.Profile.setText(_translate("Order_2", "Profile"))
        self.ProductLabel.setText(_translate("Order_2", "Order List"))
        self.manageLabel.setText(_translate("Order_2", "Manage your orders"))
        self.AddProduct.setText(_translate("Order_2", "Add New Order"))
        self.Search.setText(_translate("Order_2", "Search"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Order_2", "Order ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Order_2", "Customer Code"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Order_2", "Category"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Order_2", "Product Name"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Order_2", "Roll Size"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Order_2", "Quantity"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Order_2", "Amount Total"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Order_2", "Order Date"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Order_2", "Date Completion"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Order_2", "Actions"))

import font_rc
import images_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Order_2 = QtWidgets.QMainWindow()
    ui = Ui_Order_2()
    ui.setupUi(Order_2)
    Order_2.show()
    sys.exit(app.exec_())
