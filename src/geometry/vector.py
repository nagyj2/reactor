
import math
from copy import deepcopy

from .constants import EPSILON
from .coordinate import Coordinate

# todo:
# add .coordinates accessor
# replace with data classes?


class Vector:
    '''Handles a vector on a 2D plane with origin of (0,0).'''
    x = Coordinate()
    y = Coordinate()

    @staticmethod
    def from_polar_degrees(magnitude, degrees):
        return Vector(magnitude * math.cos(math.radians(degrees)), magnitude * math.sin(math.radians(degrees)))

    @staticmethod
    def from_polar_radians(magnitude, radians):
        return Vector(magnitude * math.cos(radians), magnitude * math.sin(radians))

    @staticmethod
    def from_origin(point):
        return Vector(point.x, point.y)

    @staticmethod
    def from_positions(point1, point2):
        return Vector(point2.x - point1.x, point2.y - point1.y)

    @staticmethod
    def unit_horizontal():
        return Vector(1, 0)

    @staticmethod
    def unit_vertical():
        return Vector(0, 1)

    @staticmethod
    def unit_diagonal():
        return Vector(1, 1).normalize()

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{type(self).__name__}(dx={self.x}, dy={self.y})'

    def __str__(self):
        return f'[{self.x}, {self.y}]'

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise TypeError(f'unsupported operand type(s) for +: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __sub__(self, other):
        if isinstance(other, Vector):
            # vector subtraction
            return Vector(self.x - other.x, self.y - other.y)
        raise TypeError(f'unsupported operand type(s) for -: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __mul__(self, other):
        if isinstance(other, Vector):  # dot product
            try:
                return self.dot(other)
            except TypeError:
                pass
        elif isinstance(other, bool):  # disallow bool since it inherits from int
            pass
        elif isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        raise TypeError(f'unsupported operand type(s) for *: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __truediv__(self, other):
        if isinstance(other, bool):  # disallow bool since it inherits from int
            pass
        elif isinstance(other, (int, float)):
            # vector scaling
            return Vector(self.x / other, self.y / other)
        raise TypeError(f'unsupported operand type(s) for /: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __floordiv__(self, other):
        if isinstance(other, bool):  # disallow bool since it inherits from int
            pass
        elif isinstance(other, (int, float)):
            return Vector(self.x // other, self.y // other)
        raise TypeError(f'unsupported operand type(s) for //: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __lt__(self, other):
        if isinstance(other, Vector):
            return self.magnitude < other.magnitude
        raise TypeError(f'\'<\' not supported between instances of \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    def __le__(self, other):
        if isinstance(other, Vector):
            return self.magnitude <= other.magnitude
        raise TypeError(f'\'<=\' not supported between instances of \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    def __eq__(self, other):
        if isinstance(other, Vector):
            # Allow sufficiently small differences to match
            return abs(self.x - other.x) < EPSILON and abs(self.y - other.y) < EPSILON
        return False

    # def __ne__(self, other):
    #     if isinstance(other, Vector):
    #         return self.x != other.x or self.y != other.y
    #     return True

    # def __ge__(self, other):
    #     if isinstance(other, Vector):
    #         return self.magnitude >= other.magnitude
    #     raise TypeError(f'\'>=\' not supported between instances of \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    # def __gt__(self, other):
    #     if isinstance(other, Vector):
    #         return self.magnitude > other.magnitude
    #     raise TypeError(f'\'>\' not supported between instances of \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self.x = self.x + other.x
            self.y = self.y + other.y
            return self
        raise TypeError(f'unsupported operand type(s) for +=: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __isub__(self, other):
        if isinstance(other, Vector):
            self.x = self.x - other.x
            self.y = self.y - other.y
            return self
        raise TypeError(f'unsupported operand type(s) for -=: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __imul__(self, other):
        if isinstance(other, bool):  # disallow bool since it inherits from int
            pass
        elif isinstance(other, (int, float)):
            self.x = self.x * other
            self.y = self.y * other
            return self
        raise TypeError(f'unsupported operand type(s) for *=: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __itruediv__(self, other):
        if isinstance(other, bool):  # disallow bool since it inherits from int
            pass
        elif isinstance(other, (int, float)):
            self.x = self.x / other
            self.y = self.y / other
            return self
        raise TypeError(f'unsupported operand type(s) for /=: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __ifloordiv__(self, other):
        if isinstance(other, bool):  # disallow bool since it inherits from int
            pass
        elif isinstance(other, (int, float)):
            self.x = self.x // other
            self.y = self.y // other
            return self
        raise TypeError(f'unsupported operand type(s) for //=: \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def as_cartesian(self):
        return self.x, self.y

    @property
    def magnitude(self):
        return math.dist((0, 0), (self.x, self.y))

    @property
    def angle(self):
        return math.degrees(math.atan2(self.y, self.x))

    def normalize(self):
        self /= self.magnitude
        return self

    def as_polar(self):
        return self.magnitude, self.angle

    def dot(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        raise TypeError(f'unsupported operand type(s) for dot(): \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    def cross(self, other):
        if isinstance(other, Vector):
            return self.x * other.y - self.y * other.x
        raise TypeError(f'unsupported operand type(s) for cross(): \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    def angle_between(self, other):
        if isinstance(other, Vector):
            return math.degrees(math.acos(self.dot(other) / (self.magnitude * other.magnitude)))
        raise TypeError(f'unsupported operand type(s) for angle_between(): \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501
