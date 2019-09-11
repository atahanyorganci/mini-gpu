from app.display.transition import Transition


class Rectangle:

    def __init__(self, position, properties):
        super().__init__()
        self.position = position
        self.property = properties
        self.transition = Transition()

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
