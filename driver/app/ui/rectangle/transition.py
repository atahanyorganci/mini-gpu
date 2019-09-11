from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QFormLayout, QLabel, QPushButton, \
    QSpinBox

from app.config import Display
from app.display.position import Position


class TransitionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config = TransitionConfigWidget()
        self.point = TransitionPointWidget()
        self.state = True
        self.init()

    def init(self):
        self.setLayout(QHBoxLayout())
        self.config.toggle_transition.connect(self.toggle)
        self.layout().addWidget(self.config)
        self.layout().addWidget(self.point)

    def data(self):
        position = self.point.data()
        enable, *rest = self.config.data()
        enable = enable and bool(position)
        return (enable, *rest, position)

    @pyqtSlot(bool)
    def toggle(self, state):
        self.state = state
        self.point.setEnabled(self.state)


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
        layout = QFormLayout()
        self.enable.setChecked(True)
        self.enable.toggled.connect(self.toggle)
        layout.addRow(QLabel("Enable transitions"), self.enable)
        self.loop.setChecked(True)
        layout.addRow(QLabel("Loop"), self.loop)
        self.rate.setSingleStep(50)
        self.rate.setMinimum(5)
        self.rate.setMaximum(1000)
        layout.addRow(QLabel("Refresh Rate (ms)"), self.rate)
        self.count.setMaximum(1000)
        layout.addRow(QLabel("Screen Count"), self.count)
        self.setLayout(layout)

    def data(self) -> tuple:
        return self.enable.isChecked(), self.loop.isChecked(), self.rate.value(), self.count.value()

    @pyqtSlot()
    def toggle(self):
        state = self.enable.isChecked()
        self.loop.setEnabled(state)
        self.rate.setEnabled(state)
        self.count.setEnabled(state)
        self.toggle_transition.emit(state)


class TransitionPointWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.point = PointWidget()
        self.container = PointViewContainerWidget()
        self.init()

    def init(self):
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Points"))
        self.layout().addWidget(self.point)
        self.point.added.connect(self.container.add_point)
        self.layout().addWidget(self.container)

    def data(self):
        return [Position(point.x, point.y) for point in self.container.points]


class PointViewContainerWidget(QWidget):

    @pyqtSlot(int, int)
    def add_point(self, x, y):
        point = PointViewWidget(x, y, len(self.points))
        point.remove.connect(self.remove_point)
        self.points.append(point)
        self.layout().addWidget(point)

    @pyqtSlot(int)
    def remove_point(self, index):
        self.layout().removeWidget(self.points.pop(index))

    def __init__(self):
        super().__init__()
        self.points = []
        self.setLayout(QVBoxLayout())


class PointViewWidget(QWidget):
    remove = pyqtSignal([int])

    def __init__(self, horizontal, vertical, index):
        super().__init__()
        self.x = horizontal
        self.y = vertical
        self.index = index
        self.button = QPushButton("Remove")
        self.init()

    def init(self):
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(QLabel(f"H. Position: {str(self.x)}"))
        self.layout().addWidget(QLabel(f"V. Position: {str(self.y)}"))
        self.button.clicked.connect(self.on_click)
        self.layout().addWidget(self.button)

    @pyqtSlot()
    def on_click(self):
        self.remove.emit(self.index)


class PointWidget(QWidget):
    added = pyqtSignal([int, int])

    def __init__(self):
        super().__init__()
        self.add = QPushButton("Add")
        self.horizontal = QSpinBox()
        self.vertical = QSpinBox()
        self.init()

    def init(self):
        layout = QHBoxLayout()
        self.horizontal.setMaximum(Display.WIDTH)
        layout.addWidget(self.horizontal)
        self.vertical.setMaximum(Display.HEIGHT)
        layout.addWidget(self.vertical)
        self.add.clicked.connect(self.on_click)
        layout.addWidget(self.add)
        self.setLayout(layout)

    @pyqtSlot()
    def on_click(self):
        self.added.emit(self.horizontal.value(), self.vertical.value())
