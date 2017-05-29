import math


class Vector:
    def __init__(self, *components: float):
        self.components = list(components)

    def scale(self, scalar: int) -> 'Vector':
        self.components = list(map(lambda x: x * scalar, self.components))
        return self

    def add(self, other: 'Vector') -> 'Vector':
        self.components = list(map(lambda z: z[0] + z[1], zip(self.components, other.components)))
        return self

    def sub(self, other: 'Vector') -> 'Vector':
        return self.add(other.scale(-1))

    def dot(self, other: 'Vector') -> float:
        return sum(map(lambda z: z[0] + z[1], zip(self.components, other.components)))

    def norm(self) -> float:
        return math.sqrt(sum(map(lambda x: x ** 2, self.components)))

    def __add__(self, other):
        if isinstance(other, Vector):
            self.add(other)
            return self

    def __sub__(self, other):
        if isinstance(other, Vector):
            self.sub(other)
            return self

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.dot(other)
        elif isinstance(other, int):
            self.scale(other)
            return self

    def __str__(self):
        return self.components.__str__()

    @staticmethod
    def span(one: 'Vector', two: 'Vector') -> 'Vector':
        return Vector(*map(lambda z: z[0] - z[1], zip(two.components, one.components)))

    @staticmethod
    def distance(one: 'Vector', two: 'Vector') -> float:
        return Vector.span(one, two).norm()
