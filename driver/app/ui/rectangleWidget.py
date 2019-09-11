import serial
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QSlider

from app.display.rectangle import Rectangle
from app.ui.transitionWidget import TransitionWidget


class RectangleWidget(QWidget):
    rectangle: Rectangle
    config: dict

    def __init__(self):
        super().__init__()
        self.properties = PropertiesWidget()
        self.position = PositionWidget()
        self.validate = QPushButton("Validate")
        self.transition = TransitionWidget()
        self.send = QPushButton("Send")
        self.timer = QBasicTimer()
        self.port = serial.Serial()
        self.init()

    def init(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Properties"))
        self.layout().addWidget(self.properties)
        self.layout().addWidget(QLabel("Position"))
        self.layout().addWidget(self.position)
        self.validate.clicked.connect(self.on_validate)
        self.layout().addWidget(self.validate)
        self.layout().addWidget(QLabel("Transition"))
        self.layout().addWidget(self.transition)
        self.send.clicked.connect(self.on_send)
        self.layout().addWidget(self.send)

    def configure(self, config):
        self.config = config
        self.port = serial.Serial(**self.config)

    def on_send(self):
        if bool(self.config) and self.__validate():
            enable, loop, rate, count, positions = self.transition.data()
            if enable:
                for position in positions:
                    self.rectangle.add_transition(loop, count, position)
                iter(self.rectangle)
                self.timer.start(rate, self)
            if not self.port.is_open:
                self.port.open()
            self.port.write(bytes(self.rectangle))

    def timerEvent(self, event) -> None:
        try:
            next(self.rectangle)
            self.port.write(bytes(self.rectangle))
        except StopIteration:
            self.timer.stop()
            self.port.close()

    def on_validate(self):
        if not self.__validate():
            self.position.reset()
            self.properties.reset()

    def __validate(self):
        try:
            pos = self.position.data()
            prop = self.properties.data()
            self.rectangle = Rectangle(*pos, *prop)
        except ValueError:
            return False
        return True


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

    def reset(self):
        self.hcorner.clear()
        self.vcorner.clear()

    def data(self) -> tuple:
        return int(self.hcorner.text()), int(self.vcorner.text())


class PropertiesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.width = QLineEdit()
        self.height = QLineEdit()
        self.red = QSlider(1)
        self.green = QSlider(1)
        self.blue = QSlider(1)
        self.init()

    def reset(self):
        self.width.clear()
        self.height.clear()

    def init(self):
        layout = QFormLayout()
        layout.addRow(QLabel('Width'), self.width)
        layout.addRow(QLabel('Height'), self.height)
        self.red.setMaximum(15)
        layout.addRow(QLabel('Red'), self.red)
        self.green.setMaximum(15)
        layout.addRow(QLabel('Green'), self.green)
        self.blue.setMaximum(15)
        layout.addRow(QLabel('Blue'), self.blue)
        self.setLayout(layout)

    def data(self) -> tuple:
        return int(self.width.text()), int(self.height.text()), \
               self.red.value(), self.green.value(), self.blue.value()
