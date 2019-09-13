from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QFormLayout, QLabel, QPushButton, QSpinBox, \
    QFrame

from app.config import Display
from app.display.position import Position


class TransitionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config = TransitionConfigWidget()
        self.list = ListWidget()
        self.init()

    def init(self):
        self.setLayout(QHBoxLayout())
        self.config.toggle_transition.connect(self.toggle)
        self.layout().addWidget(self.config)
        self.layout().addWidget(self.list)

    def data(self) -> tuple:
        positions = self.list.data()
        config, loop, rate, count = self.config.data()
        enable = config and bool(positions)
        return enable, loop, rate, count, positions

    def toggle(self, state):
        self.list.setEnabled(state)


class TransitionConfigWidget(QWidget):
    toggle_transition = pyqtSignal([bool])

    def __init__(self):
        super().__init__()
        self.enable = QCheckBox()
        self.loop = QCheckBox()
        self.rate = QSpinBox()
        self.count = QSpinBox()
        self.init()

    def init(self):
        # Add Widgets
        self.setLayout(QFormLayout())
        self.layout().addRow(QLabel("Enable transitions"), self.enable)
        self.layout().addRow(QLabel("Screen Count"), self.count)
        self.layout().addRow(QLabel("Loop"), self.loop)
        self.layout().addRow(QLabel("Refresh Rate (ms)"), self.rate)

        # Configure Widgets
        self.enable.setChecked(True)
        self.enable.toggled.connect(self.on_enable)
        self.loop.setChecked(True)
        self.rate.setSingleStep(10)
        self.rate.setMinimum(20)
        self.rate.setMaximum(1000)
        self.count.setMinimum(20)
        self.count.setMaximum(200)
        self.count.setValue(5)

    def data(self) -> tuple:
        return self.enable.isChecked(), self.loop.isChecked(), self.rate.value(), self.count.value()

    def on_enable(self):
        state = self.enable.isChecked()
        self.loop.setEnabled(state)
        self.rate.setEnabled(state)
        self.count.setEnabled(state)
        self.toggle_transition.emit(state)


class ListWidget(QWidget):
    added = pyqtSignal([int, int])

    def __init__(self):
        super().__init__()
        self.positions = []
        self.add = QPushButton("Add")
        self.horizontal = QSpinBox()
        self.vertical = QSpinBox()
        self.init()

    def init(self):
        # Add widgets
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Transition Points"))
        config = QFrame()
        config.setLayout(QHBoxLayout())
        config.layout().addWidget(self.horizontal)
        config.layout().addWidget(self.vertical)
        config.layout().addWidget(self.add)
        self.layout().addWidget(config)

        # Configure widgets and connect signals
        self.horizontal.setMaximum(Display.WIDTH)
        self.vertical.setMaximum(Display.HEIGHT)
        self.add.clicked.connect(self.on_click)

    def on_click(self):
        pos = Position(self.horizontal.value(), self.vertical.value())
        self.positions.append(pos)
        new = PositionWidget(pos)
        new.remove.connect(self.remove)
        self.layout().addWidget(new)

    def data(self) -> list:
        return self.positions

    def remove(self, widget: QWidget):
        self.layout().removeWidget(widget)


class PositionWidget(QWidget):
    remove = pyqtSignal([QWidget])

    def __init__(self, position: Position):
        super().__init__()
        self.position = position
        self.button = QPushButton("Remove")
        self.init()

    def init(self):
        # Add widgets
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(QLabel(str(self.position)))
        self.layout().addWidget(self.button)

        # Connect Signals
        self.button.clicked.connect(self.on_click)

    def on_click(self):
        self.remove.emit(self)
