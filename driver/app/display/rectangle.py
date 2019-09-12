from app.display.transition import Transition
from app.display.position import Position
from app.display.property import Property


class Rectangle:

    def __init__(self, position: Position, properties: Property, transition=Transition()):
        super().__init__()
        self.position = position
        self.property = properties
        self.transition = transition

    def __str__(self):
        return f"Rectangle(properties={str(self.property)}, position={str(self.position)})"

    def configure_transition(self, loop: int, count: int):
        self.transition.configure(loop, count)

    def remove_transition(self, position: Position):
        self.transition.remove_point(position)

    def add_transition(self, position: Position):
        if not bool(self.transition):
            self.transition.add_point(self.position)
        self.transition.add_point(position)

    def reset_transition(self):
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
