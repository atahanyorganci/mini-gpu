import sys

from PyQt5.QtWidgets import QApplication

from app.controller.serial import SerialController
from app.ui.main import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = App()
    controller = SerialController()
    controller.state.connect(view.serial_state)
    controller.error.connect(view.on_error)
    view.connect(open=controller.open, close=controller.close, write=controller.write, configure=controller.configure)
    sys.exit(app.exec_())
