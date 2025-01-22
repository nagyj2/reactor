
from .image_simple import SimpleImage
from .shapes import Rectangle


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
