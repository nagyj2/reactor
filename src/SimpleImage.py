
from Geometry import Point
from Image import Image
from Shapes import Circle, Rectangle


class SimpleImage(Image):
    '''Convinience class for images with 1 shape. Shortcuts several operations on Image.'''
    _base_name = 'base'

    def __init__(self, bx, by, shape):
        super().__init__(bx, by)
        shape.move_to(Point(bx, by))
        self[self._base_name] = shape

    def __getitem__(self, name):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot retreive additional shape \'{name}\'')
        return super().__getitem__(name)

    def __setitem__(self, name, shape):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot assign additional shape \'{name}\'')
        return super().__setitem__(name, shape)

    def __delitem__(self, name):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot retreive additional shape \'{name}\'')
        raise AttributeError(f'{type(self).__name__} cannot have only shape removed')

    @property
    def color(self):
        return self[self._base_name].color

    @color.setter
    def color(self, color):
        self[self._base_name].color = color

    @property
    def offset(self):
        return self[self._base_name].offset

    @offset.setter
    def offset(self, offset):
        self[self._base_name].offset = offset

    @property
    def layer(self):
        return self[self._base_name].layer

    @layer.setter
    def layer(self, layer):
        self[self._base_name].layer = layer


class CircleImage(SimpleImage):
    def __init__(self, bx, by, color, radius):
        shape = Circle(ox=0,
                       oy=0,
                       color=color,
                       radius=radius)
        super().__init__(bx, by, shape)

    @property
    def radius(self):
        return self[self._base_name].radius

    @radius.setter
    def radius(self, radius):
        self[self._base_name].radius = radius


class RectangleImage(SimpleImage):
    def __init__(self, bx, by, color, width, height):
        shape = Rectangle(ox=0,
                          oy=0,
                          color=color,
                          width=width,
                          height=height)
        super().__init__(bx, by, shape)

    @property
    def width(self):
        return self[self._base_name].width

    @width.setter
    def width(self, width):
        self[self._base_name].width = width

    @property
    def height(self):
        return self[self._base_name].height

    @height.setter
    def height(self, height):
        self[self._base_name].height = height

    @property
    def center(self):
        return self[self._base_name].center

    @property
    def left_x(self):
        return self[self._base_name].left_x

    @property
    def right_x(self):
        return self[self._base_name].right_x

    @property
    def bottom_y(self):
        return self[self._base_name].bottom_y

    @property
    def top_y(self):
        return self[self._base_name].top_y

    @property
    def top_left(self):
        return self[self._base_name].top_left

    @property
    def top_right(self):
        return self[self._base_name].top_right

    @property
    def bottom_left(self):
        return self[self._base_name].bottom_left

    @property
    def bottom_right(self):
        return self[self._base_name].bottom_right
