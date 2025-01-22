
from copy import deepcopy

from .constants import EPSILON
from .coordinate import Coordinate
from .vector import Vector


class Point:
    '''Handles a 2D point on the screen.'''
    x = Coordinate()
    y = Coordinate()

    @staticmethod
    def from_origin(vector):
        return Point(vector.x, vector.y)

    @staticmethod
    def from_coordinates(x_y):
        return Point(x_y[0], x_y[1])

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{type(self).__name__}(x={self.x}, y={self.y})'

    def __str__(self):
        return f'({round(self.x, 2)}, {round(self.y, 2)})'

    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError(f'unsupported operand type(s) for +: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        raise TypeError(f'unsupported operand type(s) for -: \'{type(self).__name__}\' and \'{type(other).__name__}\'')

    def __eq__(self, other):
        if isinstance(other, Point):
            # Allow sufficiently small differences to match
            return abs(self.x - other.x) < EPSILON and abs(self.y - other.y) < EPSILON
        return False

    # def __ne__(self, other):
    #     if isinstance(other, Point):
    #         return self.x != other.x or self.y != other.y
    #     return True

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

    @property
    def coordinates(self):
        return self.x, self.y

    @coordinates.setter
    def coordinates(self, x_y):
        self.x = x_y[0]
        self.y = x_y[1]
