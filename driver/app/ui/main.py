from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QMessageBox

from app.ui.rectangle.widget import RectangleTabWidget
from app.ui.serial import SerialWidget


class App(QWidget):
    error: QMessageBox
    serial_state = pyqtSignal(bool, bool)

    def __init__(self):
        super().__init__()
        self.rectangleWidget = RectangleTabWidget()
        self.serialWidget = SerialWidget()
        self.init()

    def init(self):
        self.setWindowTitle('Mini GPU Driver')
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.serialWidget)
        self.serial_state.connect(self.on_state)
        self.layout().addWidget(self.rectangleWidget)
        self.show()

    def connect(self, open: callable = None, configure: callable = None, close: callable = None,
                write: callable = None):
        if configure is not None:
            self.serialWidget.serial_configure.connect(configure)
        if open is not None:
            self.serialWidget.serial_open.connect(open)
        if close is not None:
            self.serialWidget.serial_close.connect(close)
        if write is not None:
            self.rectangleWidget.serial_write.connect(write)

    def on_state(self, configured: bool, connected: bool):
        self.serialWidget.on_state(configured=configured, connected=connected)

    def on_error(self, message: str, info: str):
        self.error = QMessageBox()
        self.error.setWindowTitle("Error")
        self.error.setIcon(QMessageBox.Critical)
        self.error.setText(message)
        self.error.setInformativeText(info)
        self.error.show()
