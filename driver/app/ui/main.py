from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.ui.rectangle.widget import RectangleWidget
from app.ui.serial import SerialWidget


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.rectangleWidget = RectangleWidget()
        self.serialWidget = SerialWidget()
        self.init()

    def init(self):
        self.setWindowTitle('Mini GPU Driver')
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.serialWidget)
        self.layout().addWidget(self.rectangleWidget)
        self.show()
