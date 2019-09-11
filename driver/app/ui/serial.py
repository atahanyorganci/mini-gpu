from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout

from app.config import Serial


class SerialWidget(QWidget):
    serial_configure = pyqtSignal([dict])
    serial_open = pyqtSignal()
    serial_close = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.configuration = {}
        self.configured = False
        self.connected = False

        self.state = QLabel()
        self.port = QLineEdit()
        self.baud_rate = QComboBox()
        self.byte_size = QComboBox()
        self.parity = QComboBox()
        self.stop_bit = QComboBox()
        self.default = QPushButton("Default")
        self.configure = QPushButton("Configure")
        self.open = QPushButton("Connect")
        self.close = QPushButton("Disconnect")

        self.init()

    def init(self):
        self.setLayout(QFormLayout())
        # Add widgets
        self.layout().addWidget(QLabel("Serial Communication Configuration"))
        self.layout().addRow(QLabel("Port"), self.port)
        self.baud_rate.addItems([str(rate) for rate in Serial.BAUD_RATE])
        self.layout().addRow(QLabel("Baud Rate"), self.baud_rate)
        self.byte_size.addItems(Serial.BYTE_SIZE.keys())
        self.layout().addRow(QLabel("Data Width"), self.byte_size)
        self.parity.addItems(Serial.PARITY.keys())
        self.layout().addRow(QLabel("Parity"), self.parity)
        self.stop_bit.addItems(Serial.STOP_BIT.keys())
        self.layout().addRow(QLabel("Stop Bits"), self.stop_bit)
        buttons = QHBoxLayout()
        buttons.addWidget(self.default)
        buttons.addWidget(self.configure)
        buttons.addWidget(self.open)
        buttons.addWidget(self.close)
        self.set_button_state()
        self.layout().addRow(buttons)

        # Connect Signals
        self.default.clicked.connect(self.on_default)
        self.configure.clicked.connect(self.on_configure)
        self.open.clicked.connect(self.on_open)
        self.close.clicked.connect(self.on_close)

    def set_button_state(self):
        self.default.setEnabled(not self.connected)
        self.configure.setEnabled(not self.connected)
        self.open.setEnabled(self.configured and not self.connected)
        self.close.setEnabled(self.connected)

    def on_default(self):
        # These are magic numbers should be changed when changing constants in controller.__init__ file
        self.port.setText("COM4")
        self.baud_rate.setCurrentIndex(16)
        self.byte_size.setCurrentIndex(3)
        self.parity.setCurrentIndex(0)
        self.stop_bit.setCurrentIndex(0)

    def on_configure(self):
        self.serial_configure.emit({"port": self.port.text(),
                                    "bytesize": Serial.BYTE_SIZE[self.byte_size.currentText()],
                                    "baudrate": Serial.BAUD_RATE[self.baud_rate.currentIndex()],
                                    "parity": Serial.PARITY[self.parity.currentText()],
                                    "stopbits": Serial.STOP_BIT[self.stop_bit.currentText()]})

    def on_open(self):
        self.serial_open.emit()
        self.connected = True
        self.set_button_state()

    def on_close(self):
        self.serial_close.emit({})
        self.connected = False
        self.set_button_state()
