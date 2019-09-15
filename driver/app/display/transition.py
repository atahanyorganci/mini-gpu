from app.display.position import Position


class Transition:

    def __init__(self):
        self.__loop = False
        self.__count = 0
        self.__points = []
        self.__ipoints = []

    def configure(self, loop: bool, count: int):
        self.__loop = bool(loop)
        self.__count = int(count)

    def add_point(self, new):
        if type(new) == Position:
            self.__points.append(new)
        else:
            raise ValueError

    def remove_point(self, point):
        self.__points.remove(point)

    def __iter__(self):
        for i, point in enumerate(self.__points):
            if i == 0:
                previous = point
                continue
            self.__generate(previous, point)
            previous = point
        if self.__loop:
            self.__generate(self.__points[-1], self.__points[0])
        return self

    def __next__(self):
        try:
            return self.__ipoints.pop(0)
        except IndexError:
            raise StopIteration

    def __generate(self, first: Position, second: Position):
        dist = second - first
        speed = Position(dist.x // self.__count, dist.y // self.__count)
        if not self.__ipoints:
            self.__ipoints.append(Position.copy(first))
        for _ in range(self.__count - 1):
            self.__ipoints.append(self.__ipoints[-1] + speed)
        self.__ipoints.append(Position.copy(second))

    def __bool__(self):
        return bool(self.__points) and bool(self.__count)
