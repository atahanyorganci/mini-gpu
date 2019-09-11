from app.display.position import Position
from app.display.property import Property
from app.display.transition import Transition


class Rectangle:

    def __init__(self, hcorner, vcorner, width, height, red, green, blue):
        super().__init__()
        self.position = Position(hcorner, vcorner)
        self.property = Property(width, height, red, green, blue)
        self.transition = Transition()
        self.iter = None

    def __str__(self):
        return f"Rectangle(properties={str(self.property)}, position={str(self.position)}"

    def add_transition(self, loop, count, *positions):
        self.transition.configure(loop, count)
        if not bool(self.transition):
            self.transition.add_point(self.position)
        for position in positions:
            self.transition.add_point(position)

    def remove_transition(self):
        self.transition = Transition()

    def __iter__(self):
        iter(self.transition)
        return self

    def __next__(self):
        try:
            position = next(self.transition)
            self.position = position
        except StopIteration:
            raise StopIteration
        return self

    def __bytes__(self):
        return bytes([1]) + bytes(self.property) + bytes(self.position)
