import pyglet

from geometry import Point

from .shapes import Shape


class Rectangle(Shape):
    def __init__(self, ox, oy, color, width, height):
        shape = pyglet.shapes.Rectangle(x=ox,
                                        y=oy,
                                        width=width,
                                        height=height,
                                        color=color)
        super().__init__(ox, oy, shape)

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return super().__eq__(other) \
                and self.width == other.width \
                and self.height == other.height
        return False

    def __repr__(self):
        return f'{type(self).__name__}(x={self.pos.x}, y={self.pos.y}, w={self.width}, h={self.height})'

    @property
    def width(self):
        return self.primitive.width

    @width.setter
    def width(self, width):
        self.primitive.width = width

    @property
    def height(self):
        return self.primitive.height

    @height.setter
    def height(self, height):
        self.primitive.height = height

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
