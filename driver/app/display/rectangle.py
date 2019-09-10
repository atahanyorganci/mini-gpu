from app.config import Display
from app.display.position import Position
from PyQt5.QtCore import QBasicTimer, QObject, pyqtSignal


class Rectangle(QObject):
    timer: QBasicTimer
    velocity: Position
    index: int

    def __init__(self, position: Position, width, height, red, green, blue):
        super().__init__()
        if position.x < 0 or position.x > Display.WIDTH or position.y < 0 or position.y > Display.HEIGHT:
            raise ValueError
        if red < 0 or red > 15 or green < 0 or green > 15 or blue < 0 or blue > 15:
            raise ValueError
        self.positions = [Position(position.x, position.y)]
        self.position = self.positions[0]
        self.width = width
        self.height = height
        self.red = red
        self.green = green
        self.blue = blue
        self.loop = False
        self.interval = 50
        self.count = 0
        self.current = 0
        self.index = 0
        self.send = pyqtSignal([bytes])

    def __str__(self):
        return f"Rectangle(current={str(self.position)}, positions={str(self.positions)}"

    def add_transition(self, loop, interval, count, *positions):
        self.loop = loop
        self.interval = interval
        self.count = count
        self.positions += positions

    def remove_transition(self):
        self.loop = False
        self.interval = 50
        self.count = 0
        self.positions = [Position(self.position.x, self.position.y)]

    def calculate(self):
        diff = self.positions[self.index + 1] - self.positions[self.index]
        self.velocity = Position(diff.x / self.count, diff.y / self.count)

    def start(self):
        self.send.emit(bytes(self))
        self.timer = QBasicTimer()
        self.calculate()
        self.timer.start(self.interval, self)

    def stop(self):
        self.timer.stop()

    def timerEvent(self, event) -> None:
        self.position += self.velocity
        if self.current < self.count:
            self.current += 1
        else:
            self.index += 1
            next_pos = self.positions[self.index]
            self.position = Position(next_pos.x, next_pos.y)
            self.timer.stop()
        self.send.emit(bytes(self))

    def __bytes__(self):
        return bytes([1, self.red, self.green, self.blue,
                      self.position.x % 256, self.position.x // 256, self.position.y % 256, self.position.y // 256,
                      self.width % 256, self.width // 256, self.height % 256, self.height // 256])
