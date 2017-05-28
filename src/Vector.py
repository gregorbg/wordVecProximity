import math


class Vector:
    def __init__(self, *components: int):
        self.components = list(components)

    def scale(self, scalar: int) -> 'Vector':
        self.components = map(lambda x: x * scalar, self.components)
        return self

    def add(self, other: 'Vector') -> 'Vector':
        for i in range(0, len(self.components)):
            self.components[i] = self.components[i] + other.components[i]

        return self

    def sub(self, other: 'Vector') -> 'Vector':
        return self.add(other.scale(-1))

    def dot(self, other: 'Vector') -> int:
        dot = 0

        for i in range(0, len(self.components)):
            dot += self.components[i] * other.components[i]

        return dot

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

    @staticmethod
    def span(one: 'Vector', two: 'Vector') -> 'Vector':
        span = []

        for i in range(0, len(one.components)):
            span[i] = two.components[i] - one.components[i]

        return Vector(*span)  # * is vararg unpacking

    @staticmethod
    def distance(one: 'Vector', two: 'Vector') -> float:
        return Vector.span(one, two).norm()
