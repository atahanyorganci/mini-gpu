from PyQt5.QtCore import QObject, pyqtSlot
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import serial


class Wrapper(QObject):

    def __init__(self):
        super(Wrapper, self).__init__()
        self.serial = serial.Serial()

    def configure(self, port="", baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE):
        self.serial = serial.Serial(baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits)
        if port != "":
            self.serial.port = port

    def open(self):
        self.serial.open()

    def close(self):
        self.serial.close()

    def write_bytes(self, sequence):
        print(bytes(sequence))
        self.serial.writelines(sequence)
