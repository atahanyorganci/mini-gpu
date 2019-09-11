from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.serial import Serial
from app.ui.rectangleWidget import RectangleWidget
from app.ui.serialWidget import SerialWidget


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.rectangleWidget = RectangleWidget()
        self.serialWidget = SerialWidget()
        self.serial = Serial
        self.init()

    def init(self):
        self.setWindowTitle('Mini GPU Driver')
        self.setGeometry(0, 0, 320, 200)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.rectangleWidget)
        self.layout().addWidget(self.serialWidget)
        self.show()
