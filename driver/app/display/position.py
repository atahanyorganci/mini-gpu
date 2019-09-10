class Position:

    def __init__(self, horizontal: int, vertical: int) -> None:
        self.x = int(horizontal)
        self.y = int(vertical)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"Position(x={self.x}, y={self.y})"

    def __repr__(self):
        return str(self)
