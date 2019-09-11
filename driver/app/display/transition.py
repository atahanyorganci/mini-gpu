from app.display.position import Position


class Transition:

    def __init__(self):
        self.loop = False
        self.count = 0
        self.__points = []
        self.__ipoints = []

    def configure(self, loop: bool, count: int):
        self.loop = bool(loop)
        self.count = int(count)

    def add_point(self, point):
        if type(point) != Position:
            raise ValueError
        self.__points.append(point)

    def remove_point(self, point):
        self.__points.remove(point)

    def __iter__(self):
        for i, point in enumerate(self.__points):
            if i == 0:
                previous = point
                continue
            self.__generate(previous, point)
            previous = point
        if self.loop:
            self.__generate(self.__points[-1], self.__points[0])
        return self

    def __next__(self):
        try:
            return self.__ipoints.pop(0)
        except IndexError:
            raise StopIteration

    def __generate(self, first, second):
        dist = second - first
        speed = Position(dist.x / self.count, dist.y / self.count)
        if not self.__ipoints:
            self.__ipoints.append(first.copy())
        for _ in range(self.count - 1):
            self.__ipoints.append(self.__ipoints[-1] + speed)
        self.__ipoints.append(second.copy())

    def __bool__(self):
        return bool(self.__points) and bool(self.count)
