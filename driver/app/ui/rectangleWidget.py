from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QVBoxLayout

from app.display.rectangle import Rectangle


class RectangleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.properties = PropertiesWidget()
        self.position = PositionWidget()
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.on_click)
        self.init()

    def init(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Properties"))
        layout.addWidget(self.properties)
        layout.addWidget(QLabel("Position"))
        layout.addWidget(self.position)
        layout.addWidget(self.okButton)
        self.setLayout(layout)

    @pyqtSlot()
    def on_click(self):
        try:
            rectangle = Rectangle(*self.position.getData(), *self.properties.getData())
            print(rectangle)
        except ValueError as ex:
            print("Invalid data is entered")


class PositionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.hcorner = QLineEdit()
        self.vcorner = QLineEdit()
        self.init()

    def init(self):
        layout = QFormLayout()
        layout.addRow(QLabel('Horizontal Corner'), self.hcorner)
        layout.addRow(QLabel('Vertical Corner'), self.vcorner)
        self.setLayout(layout)

    def getData(self) -> tuple:
        return int(self.hcorner.text()), int(self.vcorner.text())


class PropertiesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.width = QLineEdit()
        self.height = QLineEdit()
        self.red = QLineEdit()
        self.green = QLineEdit()
        self.blue = QLineEdit()
        self.init()

    def init(self):
        layout = QFormLayout()
        layout.addRow(QLabel('Width'), self.width)
        layout.addRow(QLabel('Height'), self.height)
        layout.addRow(QLabel('Red'), self.red)
        layout.addRow(QLabel('Green'), self.green)
        layout.addRow(QLabel('Blue'), self.blue)
        self.setLayout(layout)

    def getData(self) -> tuple:
        return int(self.width.text()), int(self.height.text()), \
               int(self.red.text()), int(self.green.text()), int(self.blue.text())
