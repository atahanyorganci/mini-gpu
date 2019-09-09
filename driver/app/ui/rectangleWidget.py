from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QCheckBox

from app.display.rectangle import Rectangle


class RectangleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.properties = PropertiesWidget()
        self.position = PositionWidget()
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.check_rectangle)
        self.init()

    def init(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Properties"))
        layout.addWidget(self.properties)
        layout.addWidget(QLabel("Position"))
        layout.addWidget(self.position)
        layout.addWidget(self.okButton)
        self.setLayout(layout)

    def check_rectangle(self):
        try:
            rectangle = Rectangle(*self.position.data(), *self.properties.data())
            print(rectangle)
        except ValueError:
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

    def data(self) -> tuple:
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

    def data(self) -> tuple:
        return int(self.width.text()), int(self.height.text()), \
               int(self.red.text()), int(self.green.text()), int(self.blue.text())


class TransitionWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.enable = QCheckBox()
        self.loop = QCheckBox()
        self.rate = QLineEdit()
        self.init()

    def init(self):
        layout = QFormLayout()
        self.enable.setChecked(True)
        self.enable.toggled.connect(self.toggle)
        layout.addRow(QLabel("Enable transitions"), self.enable)
        self.loop.setChecked(True)
        layout.addRow(QLabel("Loop"), self.loop)
        layout.addRow(QLabel("Refresh Rate (ms)"), self.rate)
        self.setLayout(layout)

    def toggle(self):
        state = self.enable.isChecked()
        self.loop.setEnabled(state)
        self.rate.setEnabled(state)