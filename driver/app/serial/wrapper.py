import serial
from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE


class Wrapper:

    def __init__(self):
        self.serial = serial.Serial()

    def configure(self, port="COM4", baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE):
        self.serial = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits)
        if self.serial.is_open:
            self.serial.close()

    def open(self) -> None:
        self.serial.open()

    def close(self) -> None:
        self.serial.close()

    def write_bytes(self, sequence) -> None:
        print(bytes(sequence))
        for byte in bytes(sequence):
            self.serial.write(byte)

    def ready(self) -> bool:
        return self.serial.writable()
