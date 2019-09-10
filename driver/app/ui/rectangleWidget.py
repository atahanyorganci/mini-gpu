from PyQt5.QtWidgets import QWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QSlider

from app.display.rectangle import Rectangle
from app.display.position import Position
from app.ui.transitionWidget import TransitionWidget


class RectangleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.properties = PropertiesWidget()
        self.position = PositionWidget()
        self.validate = QPushButton("Validate")
        self.transition = TransitionWidget()
        self.send = QPushButton("Send")
        self.init()

    def init(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Properties"))
        layout.addWidget(self.properties)
        layout.addWidget(QLabel("Position"))
        layout.addWidget(self.position)
        self.validate.clicked.connect(self.check_rectangle)
        layout.addWidget(self.validate)
        layout.addWidget(QLabel("Transition"))
        layout.addWidget(self.transition)
        self.send.clicked.connect(self.serial_send)
        layout.addWidget(self.send)
        self.setLayout(layout)

    def serial_send(self):
        valid, r = self.check_rectangle()
        if not valid:
            return
        enable, loop, rate, dist, pos = self.transition.data()
        if enable:
            r.add_transition(loop, rate, dist, *pos)
        else:
            r.remove_transition()


    def check_rectangle(self):
        try:
            p = Position(*self.position.data())
            r = Rectangle(p, *self.properties.data())
            return True, r
        except ValueError:
            self.position.reset()
            self.properties.reset()
            return False, None


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
