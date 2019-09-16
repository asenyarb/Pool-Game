from math import sqrt
from cfg import *


class Vector:
    x: float
    y: float

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def copy(self):
        """Returns a copy a vector."""
        return Vector(self.x, self.y)

    def magnitude(self) -> float:
        """Calculates Euclidian magnitude of a vector."""
        return sqrt(self.x * self.x + self.y * self.y)

    def __add__(self, second_vector):
        return Vector(self.x + second_vector.x, self.y + second_vector.y)

    def __sub__(self, second_vector):
        return Vector(self.x - second_vector.x, self.y - second_vector.y)

    def __mul__(self, scalar: float):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __str__(self):
        return 'Vector(' + str(self.x) + ', ' + str(self.y) + ')'

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __eq__(self, second_vector):
        return self.x == second_vector.x and self.y == second_vector.y

    def normalize(self):
        """Sets a magnitude of a vector equal to 1 but preserves it's direction."""
        mag: float = self.magnitude()
        self.x /= mag
        self.y /= mag
        return self

    def set_magnitude(self, scalar):
        """Sets a magnitude of a vector equal to a given number (preserves direction)."""
        mag = self.magnitude()
        self.x = self.x * scalar / mag
        self.y = self.y * scalar / mag
        return self

    def dot(self, second_vector):
        """Dot PRODUCT of vectors (returns scalar)."""
        return self.x * second_vector.x + self.y * second_vector.y

    def u_to_pix(self):
        """Converts UNITs to pixels, flips the Y axis, returns pair of integers (tuple)."""
        return int(self.x * UNIT), HEIGHT - int(self.y * UNIT)


# def render(self, origin, color):
#    """Renders vector of a certain color relative to specified origin."""
#   pygame.draw.line(screen, color, origin.utopix(), (self+origin).utopix())
#  pygame.draw.circle(screen, color, (self+origin).utopix(), 3)
