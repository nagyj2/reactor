from image import CircleImage, RectangleImage
from util import Physics

from .graphical_entity_simple import SimpleGraphicalEntity


class PointEntity(SimpleGraphicalEntity):
    '''Base class for a 2D points.'''
    def __init__(self, x, y, dx, dy, color, radius, static=False):
        image = CircleImage(x, y, color, radius)
        super().__init__(x, y, dx, dy, image, static)

    def __contains__(self, other):
        if isinstance(other, PointEntity):
            return Physics.intersect_point_point(self, other)
        elif isinstance(other, CircleEntity):
            return Physics.intersect_point_circle(self, other)
        elif isinstance(other, RectangleEntity):
            return Physics.intersect_point_rectangle(self, other)
        raise NotImplementedError(f'unsupported type(s) for collision checking: \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    @property
    def radius(self):
        return self.image.radius

    @radius.setter
    def radius(self, radius):
        self.image.radius = radius


class CircleEntity(SimpleGraphicalEntity):
    '''Base class for a 2D circle.'''
    def __init__(self, x, y, dx, dy, color, radius, static=False):
        image = CircleImage(x, y, color, radius)
        super().__init__(x, y, dx, dy, image, static)

    def __contains__(self, other):
        if isinstance(other, PointEntity):
            return Physics.intersect_circle_point(self, other)
        elif isinstance(other, CircleEntity):
            return Physics.intersect_circle_circle(self, other)
        elif isinstance(other, RectangleEntity):
            return Physics.intersect_circle_rectangle(self, other)
        raise NotImplementedError(f'unsupported type(s) for collision checking: \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    @property
    def radius(self):
        return self.image.radius

    @radius.setter
    def radius(self, radius):
        self.image.radius = radius


class RectangleEntity(SimpleGraphicalEntity):
    '''Base class for a 2D planes.'''
    def __init__(self, x, y, dx, dy, color, w, h, static=False):
        image = RectangleImage(x, y, color, w, h)
        super().__init__(x, y, dx, dy, image, static)

        self.physics = Physics.PhysicsType.Complex

    def __contains__(self, other):
        if isinstance(other, PointEntity):
            return Physics.intersect_rectangle_point(self, other)
        elif isinstance(other, CircleEntity):
            return Physics.intersect_rectangle_circle(self, other)
        elif isinstance(other, RectangleEntity):
            return Physics.intersect_rectangle_rectangle(self, other)
        raise NotImplementedError(f'unsupported type(s) for collision checking: \'{type(self).__name__}\' and \'{type(other).__name__}\'')  # noqa: E501

    @property
    def width(self):
        return self.image.width

    @width.setter
    def width(self, width):
        self.image.width = width

    @property
    def height(self):
        return self.image.height

    @height.setter
    def height(self, height):
        self.image.height = height

    @property
    def center(self):
        return self.image.center

    @property
    def left_x(self):
        return self.image.left_x

    @property
    def right_x(self):
        return self.image.right_x

    @property
    def bottom_y(self):
        return self.image.bottom_y

    @property
    def top_y(self):
        return self.image.top_y

    @property
    def top_left(self):
        return self.image.top_left

    @property
    def top_right(self):
        return self.image.top_right

    @property
    def bottom_left(self):
        return self.image.bottom_left

    @property
    def bottom_right(self):
        return self.image.bottom_right
