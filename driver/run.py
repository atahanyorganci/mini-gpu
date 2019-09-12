import sys

from PyQt5.QtWidgets import QApplication

from app.ui.main import App
from app.controller.serial import SerialController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = App()
    controller = SerialController()
    view.connect(open=controller.open, close=controller.close, write=controller.write, configure=controller.configure)
    sys.exit(app.exec_())
