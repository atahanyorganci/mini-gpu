from PyQt5.QtCore import QBasicTimer, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QTabWidget

from app.display.rectangle import Rectangle
from app.ui.rectangle.position import PositionWidget
from app.ui.rectangle.properties import PropertiesWidget
from app.ui.rectangle.transition import TransitionWidget


class RectangleTabWidget(QWidget):
    serial_write = pyqtSignal([bytes])

    def __init__(self):
        super(RectangleTabWidget, self).__init__()
        self.setLayout(QVBoxLayout())
        self.tabs = QTabWidget()
        self.rectangles = [RectangleWidget(i) for i in range(4)]
        self.init()

    def init(self):
        for i, rectangle in enumerate(self.rectangles):
            self.tabs.addTab(rectangle, f"Rectangle {i + 1}")
            rectangle.serial_write.connect(self.serial_write)
        self.tabs.resize(500, 500)
        self.layout().addWidget(self.tabs)


class RectangleWidget(QWidget):
    iter: iter
    rectangle: Rectangle
    serial_write = pyqtSignal([bytes])

    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.properties = PropertiesWidget()
        self.position = PositionWidget()
        self.transition = TransitionWidget()
        self.send = QPushButton("Send")
        self.timer = QBasicTimer()
        self.init()

    def init(self):
        wrapper = QFrame()
        wrapper.setLayout(QHBoxLayout())
        # Properties and position
        base = QFrame()
        base.setLayout(QVBoxLayout())
        base.layout().addWidget(QLabel("Properties"))
        base.layout().addWidget(self.properties)
        base.layout().addWidget(QLabel("Position"))
        base.layout().addWidget(self.position)
        wrapper.layout().addWidget(base)
        # Transition
        transition = QFrame()
        transition.setLayout(QVBoxLayout())
        transition.layout().addWidget(QLabel("Transition"))
        transition.layout().addWidget(self.transition)
        wrapper.layout().addWidget(transition)
        # Send Button
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Rectangle Configuration"))
        self.layout().addWidget(wrapper)
        self.layout().addWidget(self.send)

        self.send.clicked.connect(self.on_send)

    def on_send(self):
        if self.timer.isActive():
            return
        pos = self.position.data()
        prop = self.properties.data()
        if pos is None or prop is None:
            return
        self.rectangle = Rectangle(self.index, pos, prop)
        enable, loop, rate, count, positions = self.transition.data()
        if enable:
            self.rectangle.reset_transition()
            self.rectangle.configure_transition(loop, count)
            for position in positions:
                self.rectangle.add_transition(position)
            self.iter = iter(self.rectangle)
            self.timer.start(rate, self)
        self.serial_write.emit(bytes(self.rectangle))

    def timerEvent(self, event) -> None:
        try:
            new = next(self.iter)
            print(new)
            self.serial_write.emit(bytes(new))
        except StopIteration:
            self.timer.stop()
