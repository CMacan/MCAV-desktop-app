import sys
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QPixmap

def load_image():
    pixmap = QPixmap(":/static/static/logo.jpg")
    if pixmap.isNull():
        print("Error: Image loading failed")
    else:
        print("Image loaded successfully")
        label = QLabel()
        label.setPixmap(pixmap)
        label.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_image()  # Call the function to load and display the image
    sys.exit(app.exec_())
