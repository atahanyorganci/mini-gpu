from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QDialog, QFormLayout, QHBoxLayout
from app.ui.serialConfigWidget import SerialConfigWidget
from serial import Serial
from app.display.rectangle import Rectangle


class SerialWidget(QWidget):
    NOT_CONFIGURED = "Not configured"

    def __init__(self, serial):
        super().__init__()

        self.serial = serial
        self.configuration = {}
        self.configured = False
        self.connected = False

        self.header = QLabel("Serial Communication Configuration")
        self.port = QLabel(SerialWidget.NOT_CONFIGURED)
        self.baud = QLabel(SerialWidget.NOT_CONFIGURED)
        self.data = QLabel(SerialWidget.NOT_CONFIGURED)
        self.parity = QLabel(SerialWidget.NOT_CONFIGURED)
        self.stop = QLabel(SerialWidget.NOT_CONFIGURED)
        self.configure = QPushButton("Configure")
        self.connect = QPushButton("Connect")
        self.disconnect = QPushButton("Disconnect")
        self.buttons = QHBoxLayout()
        self.dialog = SerialConfigWidget()

        self.init()

    def init(self):
        layout = QFormLayout()
        layout.addWidget(self.header)
        layout.addRow(QLabel("Port"), self.port)
        layout.addRow(QLabel("Baud Rate"), self.baud)
        layout.addRow(QLabel("Data Bits"), self.data)
        layout.addRow(QLabel("Parity"), self.parity)
        layout.addRow(QLabel("Stop Bits"), self.stop)
        self.set_button_state()
        self.configure.clicked.connect(self.serial_configure)
        self.buttons.addWidget(self.configure)
        self.connect.clicked.connect(self.serial_connect)
        self.buttons.addWidget(self.connect)
        self.disconnect.clicked.connect(self.serial_disconnect)
        self.buttons.addWidget(self.disconnect)
        layout.addRow(self.buttons)
        self.setLayout(layout)

    def set_button_state(self):
        self.configure.setEnabled(not self.connected)
        self.connect.setEnabled(self.configured and not self.connected)
        self.disconnect.setEnabled(self.connected)

    def serial_configure(self):
        if self.dialog.exec() == QDialog.Accepted:
            self.configuration = self.dialog.data()
            self.port.setText(self.configuration["port"])
            self.baud.setText(str(self.configuration["baudrate"]))
            self.data.setText(str(self.configuration["bytesize"]))
            self.parity.setText(str(self.configuration["parity"]))
            self.stop.setText(str(self.configuration["stopbits"]))
            self.configured = True
            self.set_button_state()

    def serial_connect(self):
        self.serial = Serial(**self.configuration)
        self.connected = True
        self.set_button_state()

    def serial_disconnect(self):
        self.serial.close()
        self.connected = False
        self.set_button_state()