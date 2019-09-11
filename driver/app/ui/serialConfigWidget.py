from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout

from app.serial import BAUD_RATE, PARITY, STOP_BIT, BYTE_SIZE


class SerialConfigWidget(QDialog):

    def __init__(self):
        super().__init__()

        self.setModal(2)
        self.setWindowTitle("Configure Serial Port")

        self.port = QLineEdit()
        self.baudrate = QComboBox()
        self.byte_size = QComboBox()
        self.parity = QComboBox()
        self.stop_bit = QComboBox()
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.defaultButton = QPushButton("Default")
        self.buttons = QHBoxLayout()

        self.init()

    def init(self):
        layout = QFormLayout()
        # Port Select
        layout.addRow(QLabel("Channel"), self.port)
        # Baud rate select
        self.baudrate.addItems([str(rate) for rate in BAUD_RATE])
        layout.addRow(QLabel("Baud Rate"), self.baudrate)
        # Data bits select
        self.byte_size.addItems(BYTE_SIZE.keys())
        layout.addRow(QLabel("Data Bits"), self.byte_size)
        # Parity select
        self.parity.addItems(PARITY.keys())
        layout.addRow(QLabel("Parity"), self.parity)
        # Stop bit select
        self.stop_bit.addItems(STOP_BIT.keys())
        layout.addRow(QLabel("Stop Bit"), self.stop_bit)
        # Buttons
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.defaultButton.clicked.connect(self.default)
        self.buttons.addWidget(self.okButton)
        self.buttons.addWidget(self.cancelButton)
        self.buttons.addWidget(self.defaultButton)
        layout.addRow(self.buttons)
        self.setLayout(layout)

    def default(self):
        # These are magic numbers should be changed when changing constants in serial.__init__ file
        self.port.setText("COM4")
        self.baudrate.setCurrentIndex(16)
        self.byte_size.setCurrentIndex(3)
        self.parity.setCurrentIndex(0)
        self.stop_bit.setCurrentIndex(0)

    def data(self):
        return {
            "port": self.port.text(),
            "bytesize": BYTE_SIZE[self.byte_size.currentText()],
            "baudrate": BAUD_RATE[self.baudrate.currentIndex()],
            "parity": PARITY[self.parity.currentText()],
            "stopbits": STOP_BIT[self.stop_bit.currentText()],
        }
