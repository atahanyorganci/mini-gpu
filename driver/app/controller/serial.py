from PyQt5.QtCore import pyqtSignal, QObject
from serial import Serial, SerialException


class SerialController(QObject):
    error = pyqtSignal(str, str)
    state = pyqtSignal(bool, bool)

    def __init__(self):
        super(SerialController, self).__init__()
        self.__serial = Serial()
        self.configured = False

    def configure(self, configuration: dict):
        try:
            self.__serial = Serial(**configuration)
            if self.__serial.is_open:
                self.__serial.close()
            self.configured = True
        except SerialException:
            self.error.emit('Serial port configuration failed.',
                            'Serial port configuration failed, try with another port.')
        finally:
            self.state.emit(self.configured, self.__serial.is_open)

    def open(self):
        try:
            if not self.__serial.is_open:
                self.__serial.open()
        except SerialException:
            self.error.emit('Serial port cannot be opened.', 'Serial port cannot be opened, port access denied.')
        finally:
            self.state.emit(self.configured, self.__serial.is_open)

    def close(self):
        try:
            if self.__serial.is_open:
                self.__serial.close()
        except SerialException:
            self.error.emit('Serial port cannot be closed.', 'Serial port cannot be closed, port is already closed.')
        finally:
            self.state.emit(self.configured, self.__serial.is_open)

    def write(self, sequence):
        try:
            self.__serial.write(bytes(sequence))
        except SerialException:
            self.error.emit('Rectangle configuration cannot be sent',
                            'Serial port must be configured and open to send bytes.')

    def ready(self) -> bool:
        return self.__serial.writable()
