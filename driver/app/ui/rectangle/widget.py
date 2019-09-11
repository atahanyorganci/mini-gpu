from PyQt5.QtCore import QBasicTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

from app.display.rectangle import Rectangle
from app.ui.rectangle.position import PositionWidget
from app.ui.rectangle.properties import PropertiesWidget
from app.ui.rectangle.transition import TransitionWidget


class RectangleWidget(QWidget):
    rectangle: Rectangle
    write = pyqtSignal([bytes])

    def __init__(self):
        super().__init__()
        self.properties = PropertiesWidget()
        self.position = PositionWidget()
        self.transition = TransitionWidget()
        self.send = QPushButton("Send")
        self.timer = QBasicTimer()
        self.init()

    def init(self):
        wrapper = QHBoxLayout()
        # Properties and position
        base = QVBoxLayout()
        base.addWidget(QLabel("Properties"))
        base.addWidget(self.properties)
        base.addWidget(QLabel("Position"))
        base.addWidget(self.position)
        wrapper.addItem(base)
        # Transition
        transition = QVBoxLayout()
        transition.addWidget(QLabel("Transition"))
        transition.addWidget(self.transition)
        wrapper.addItem(transition)
        # Send Button
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Rectangle Configuration"))
        self.layout().addItem(wrapper)
        self.layout().addWidget(self.send)

        self.send.clicked.connect(self.on_send)

    def on_send(self):
        pos = self.position.data()
        prop = self.properties.data()
        if pos is None or prop is None:
            return
        self.rectangle = Rectangle(pos, prop)
        enable, loop, rate, count, positions = self.transition.data()
        if enable:
            for position in positions:
                self.rectangle.add_transition(loop, count, position)
            iter(self.rectangle)
            self.timer.start(rate, self)
        self.write.emit(bytes(self.rectangle))

    def timerEvent(self, event) -> None:
        try:
            next(self.rectangle)
            self.write.emit(bytes(self.rectangle))
        except StopIteration:
            self.timer.stop()
            self.port.close()
