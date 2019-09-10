from app.config import Display
from app.display.position import Position


class Rectangle:
    def __init__(self, position: Position, width, height, red, green, blue):
        if position.x < 0 or position.x > Display.WIDTH or position.y < 0 or position.y > Display.HEIGHT:
            raise ValueError
        if red < 0 or red > 15 or green < 0 or green > 15 or blue < 0 or blue > 15:
            raise ValueError
        self.positions = [Position(position.x, position.y)]
        self.position = position
        self.width = width
        self.height = height
        self.red = red
        self.green = green
        self.blue = blue
        self.loop = False
        self.rate = 50
        self.dist = 0

    def __str__(self):
        return f"Rectangle(current={str(self.position)}, positions={str(self.positions)}"

    def add_transition(self, loop, rate, dist, *positions):
        self.loop = loop
        self.rate = rate
        self.dist = dist
        self.positions += positions

    def remove_transition(self):
        self.loop = False
        self.rate = 50
        self.dist = 0
        self.positions = [Position(self.position.x, self.position.y)]

    def move(self, velocity: Position):
        self.position += velocity

    def __bytes__(self):
        return bytes([1, self.red, self.green, self.blue,
                      self.position.x % 256, self.position.x // 256, self.position.y % 256, self.position.y // 256,
                      self.width % 256, self.width // 256, self.height % 256, self.height // 256])
