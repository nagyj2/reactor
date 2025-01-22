import pyglet

from .shapes import Shape


class Circle(Shape):
    def __init__(self, ox, oy, color, radius):
        shape = pyglet.shapes.Circle(x=ox,
                                     y=oy,
                                     radius=radius,
                                     color=color)
        super().__init__(ox, oy, shape)

    @property
    def radius(self):
        return self.primitive.radius

    @radius.setter
    def radius(self, radius):
        self.primitive.radius = radius

    def __eq__(self, other):
        if isinstance(other, Circle):
            return super().__eq__(other) \
                and self.radius == other.radius
        return False
