from PyQt5.QtWidgets import QWidget, QSpinBox, QSlider, QFormLayout, QLabel

from app.config import Display
from app.display.property import Property


class PropertiesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.x = QSpinBox()
        self.y = QSpinBox()
        self.red = ColorWidget()
        self.green = ColorWidget()
        self.blue = ColorWidget()
        self.init()

    def init(self):
        self.setLayout(QFormLayout())
        self.layout().addRow(QLabel('Width'), self.x)
        self.layout().addRow(QLabel('Height'), self.y)
        self.layout().addRow(QLabel('Red'), self.red)
        self.layout().addRow(QLabel('Green'), self.green)
        self.layout().addRow(QLabel('Blue'), self.blue)
        self.configure()

    def configure(self):
        self.x.setMaximum(Display.WIDTH)
        self.x.setValue(50)
        self.y.setMaximum(Display.HEIGHT)
        self.y.setValue(50)

    def data(self) -> Property:
        try:
            return Property(self.x.value(), self.y.value(), self.red.value(), self.green.value(), self.blue.value())
        except ValueError:
            self.configure()


class ColorWidget(QSlider):

    def __init__(self):
        super(ColorWidget, self).__init__()
        self.setOrientation(1)
        val = 2 ** Display.COLOR - 1
        self.setMaximum(val)
        self.setValue(val)
