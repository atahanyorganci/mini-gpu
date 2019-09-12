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

    def connect(self, open=None, configure=None, close=None, write=None):
        if configure is not None:
            self.serialWidget.serial_configure.connect(configure)
        if open is not None:
            self.serialWidget.serial_open.connect(open)
        if close is not None:
            self.serialWidget.serial_close.connect(close)
        if write is not None:
            self.rectangleWidget.serial_write.connect(write)
