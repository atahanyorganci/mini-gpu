from PyQt5.QtWidgets import QWidget, QVBoxLayout
import serial

from app.ui.rectangleWidget import RectangleWidget
from app.ui.serialWidget import SerialWidget


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.serial = serial.Serial()
        self.init()

    def init(self):
        self.setWindowTitle('Mini GPU Driver')
        self.setGeometry(50, 50, 320, 200)
        layout = QVBoxLayout()
        layout.addWidget(RectangleWidget())
        layout.addWidget(SerialWidget(self.serial))
        self.setLayout(layout)
        self.show()
