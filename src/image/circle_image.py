from .image_simple import SimpleImage
from .shapes import Circle


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
