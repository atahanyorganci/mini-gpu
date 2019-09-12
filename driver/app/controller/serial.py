import serial


class SerialController:

    def __init__(self):
        self.__serial = serial.Serial()

    def configure(self, configuration: dict):
        self.__serial = serial.Serial(**configuration)
        if self.__serial.is_open:
            self.__serial.close()

    def open(self):
        if not self.__serial.is_open:
            self.__serial.open()

    def close(self):
        if self.__serial.is_open:
            self.__serial.close()

    def write(self, sequence):
        self.__serial.write(bytes(sequence))

    def ready(self) -> bool:
        return self.__serial.writable()
