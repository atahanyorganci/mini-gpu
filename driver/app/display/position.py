from app.config import Display


class Position:

    def __init__(self, x: int, y: int):
        if x < -Display.WIDTH or x > Display.WIDTH or y < -Display.HEIGHT or y > Display.HEIGHT:
            raise ValueError
        self.x = x
        self.y = y

    @classmethod
    def copy(cls, position):
        return cls(position.x, position.y)

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self):
        return f"Position(x={self.x}, y={self.y})"

    def __repr__(self):
        return str(self)

    def __bytes__(self):
        return bytes([self.x % 256, self.x // 256, self.y % 256, self.y // 256])
