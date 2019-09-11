from PyQt5.QtWidgets import QWidget, QSpinBox, QFormLayout, QLabel

from app.config import Display
from app.display.position import Position


class PositionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.x = QSpinBox()
        self.y = QSpinBox()
        self.init()

    def init(self):
        # Add widgets
        self.setLayout(QFormLayout())
        self.layout().addRow(QLabel('Horizontal Corner'), self.x)
        self.layout().addRow(QLabel('Vertical Corner'), self.y)
        self.configure()

    def configure(self):
        self.x.setMaximum(Display.WIDTH - 1)
        self.y.setMaximum(Display.HEIGHT - 1)
        self.x.setValue(0)
        self.y.setValue(0)

    def data(self) -> Position:
        try:
            return Position(self.x.value(), self.y.value())
        except ValueError:
            self.configure()
