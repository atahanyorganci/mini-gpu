from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.ui.rectangleWidget import RectangleWidget


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Mini GPU Driver'
        self.left = 50
        self.top = 50
        self.width = 320
        self.height = 200
        self.init()

    def init(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        layout = QVBoxLayout()
        layout.addWidget(RectangleWidget())
        self.setLayout(layout)
        self.show()
