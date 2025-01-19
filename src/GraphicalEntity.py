
from copy import copy
from functools import wraps

from Entity import Entity
from Geometry import Coordinate, Point, Vector
from Image import CircleImage, ComplexImage, PointImage, RectangleImage
from Physics import GlobalPhysics as Physics

# todo:
# Performance test
#   self.image.pos.x = self.pos.x / self.image.pos.y = self.pos.y
#   self.image.pos = copy(self.pos)
# move base graphical entity to Entity


def static_update_function(f):
    '''Enforce update function assumption that object will not move.'''
    @wraps(f)
    def wrapper(self, *args, **kw):
        old_pos = copy(self.pos)
        result = f(self, *args, **kw)
        # Assert no change to position of entity
        assert self.pos == old_pos
        return result
    return wrapper


class GraphicalEntity(Entity):

    def __init__(self, x, y, dx, dy, image, static=False):
        super().__init__()
        self.pos = Point(x, y)
        self.vel = Vector(dx, dy)
        self.static = static

        self.image = image
        self.repr.append(self.image)

    def __str__(self):
        return f'{type(self).__name__}(x={self.pos.x},y={self.pos.y})'

    @static_update_function
    def _update(self, dt):
        '''Apply update logic. Does not move or draw the entity.'''
        super()._update(dt)

    def _move(self, dt):
        '''Apply simulation movement logic.'''
        self.pos += self.vel * dt

    def move(self, dt):
        if self.enable and self.alive and not self.static:
            self._move(dt)

    @static_update_function
    def _draw(self):
        '''Update graphical element properties and positions. Does not directly move or draw the entity.'''
        self.image.basepos.x = self.pos.x
        self.image.basepos.y = self.pos.y
        self.image.draw()

    def draw(self):
        if self.enable and self.alive:
            self._draw()


class PointEntity(GraphicalEntity):
    '''Base class for a 2D points.'''
    radius = Coordinate()

    def __init__(self, x, y, dx, dy, color, radius, static=False):
        image = PointImage(x, y, color, radius)
        super().__init__(x, y, dx, dy, image, static)

        self.radius = radius

    def __contains__(self, other):
        if isinstance(other, PointEntity):
            return Physics.intersect_point_point(self, other)
        elif isinstance(other, CircleEntity):
            return Physics.intersect_point_circle(self, other)
        elif isinstance(other, RectangleEntity):
            return Physics.intersect_point_rectangle(self, other)
        raise NotImplementedError(f'unsupported type(s) for collision checking: \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    @property
    def position(self):
        return Point(self.pos.x, self.pos.y)

    @static_update_function
    def _draw(self):
        self.image.radius = self.radius

        super()._draw()


class CircleEntity(GraphicalEntity):
    '''Base class for a 2D circle.'''
    radius = Coordinate()

    def __init__(self, x, y, dx, dy, color, radius, static=False):
        image = CircleImage(x, y, color, radius)
        super().__init__(x, y, dx, dy, image, static)

        self.radius = radius

    def __contains__(self, other):
        if isinstance(other, PointEntity):
            return Physics.intersect_circle_point(self, other)
        elif isinstance(other, CircleEntity):
            return Physics.intersect_circle_circle(self, other)
        elif isinstance(other, RectangleEntity):
            return Physics.intersect_circle_rectangle(self, other)
        raise NotImplementedError(f'unsupported type(s) for collision checking: \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    @static_update_function
    def _draw(self):
        self.image.radius = self.radius

        super()._draw()


class RectangleEntity(GraphicalEntity):
    '''Base class for a 2D planes.'''
    width = Coordinate()
    height = Coordinate()

    def __init__(self, x, y, dx, dy, color, w, h, static=False):
        image = RectangleImage(x, y, color, w, h)
        super().__init__(x, y, dx, dy, image, static)

        self.width = w
        self.height = h

    def __contains__(self, other):
        if isinstance(other, PointEntity):
            return Physics.intersect_rectangle_point(self, other)
        elif isinstance(other, CircleEntity):
            return Physics.intersect_rectangle_circle(self, other)
        elif isinstance(other, RectangleEntity):
            return Physics.intersect_rectangle_rectangle(self, other)
        raise NotImplementedError(f'unsupported type(s) for collision checking: \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    @property
    def center(self):
        return Point(self.pos.x + self.width/2, self.pos.y + self.height/2)

    @property
    def left_x(self):
        return self.pos.x

    @property
    def right_x(self):
        return self.pos.x + self.width

    @property
    def bottom_y(self):
        return self.pos.y

    @property
    def top_y(self):
        return self.pos.y + self.height

    @property
    def top_left(self):
        return Point(self.left_x, self.top_y)

    @property
    def top_right(self):
        return Point(self.right_x, self.top_y)

    @property
    def bottom_left(self):
        return Point(self.left_x, self.bottom_y)

    @property
    def bottom_right(self):
        return Point(self.right_x, self.bottom_y)

    @static_update_function
    def _draw(self):
        self.image.width = self.width
        self.image.height = self.height

        super()._draw()


class ComplexEntity(GraphicalEntity):
    def __init__(self, x, y, dx, dy):
        image = ComplexImage(x, y)

        super().__init__(x, y, dx, dy, image)
