from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)  # Change cursor to pointer on hover

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)