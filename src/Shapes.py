
import enum
from copy import deepcopy

import pyglet

from Geometry import Point, Vector

# todo:
# on __del__, remove from batch
# instea dof storing colour at each instance, use properties to bypass layers

shape_batch = pyglet.graphics.Batch()

shape_front = pyglet.graphics.Group(order=0)  # last to draw (top)
shape_foreground = pyglet.graphics.Group(order=1)
shape_midground = pyglet.graphics.Group(order=2)
shape_background = pyglet.graphics.Group(order=3)
shape_back = pyglet.graphics.Group(order=4)  # first to draw (bottom)

# Mapping private attributes to public arguments in pyglet shapes
# Used for deepcopy. Only includes used elements
_priv_to_pub_pyglet_shape_mapping = {
    '_x': 'x',
    '_y': 'y',
    '_radius': 'radius',
    '_rgba': 'color',
    '_batch': 'batch',
    '_user_group': 'group',
    '_width': 'width',
    '_height': 'height',
}


def draw_primitives():
    shape_batch.draw()


class Layer(enum.IntEnum):
    FRONT = 0
    FOREGROUND = 1
    MIDGROUND = 2
    BACKGROUND = 3
    BACK = 4


class Shape:
    def __init__(self, ox, oy, primitive):
        self._offset = Vector(ox, oy)
        self.primitive = primitive

    def __iter__(self):
        return self.primitive  # return to use pyglet 2.0.8's `in` integration

    def __eq__(self, other):
        if isinstance(other, Shape):
            return self.__class__ == other.__class__ \
                and self.offset == other.offset \
                and self.pos == other.pos \
                and self.color == other.color \
                and self.layer == other.layer
        return False

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
            if k == 'primitive':  # pyglet.shapes are not pickleable so recreate a fresh one
                inputs = {_priv_to_pub_pyglet_shape_mapping[pk]: pv for pk, pv in v.__dict__.items()
                          if pk in _priv_to_pub_pyglet_shape_mapping}
                new_primitive = v.__class__(**inputs)
                setattr(result, k, new_primitive)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def delete(self):
        self.primitive.destroy()

    @property
    def color(self):
        return self.primitive.color

    @color.setter
    def color(self, color):
        if len(color) == 3:  # add opacity if missing
            color = color + (255,)
        self.primitive.color = color

    def move_to(self, new_basepos):
        self.primitive.position = (new_basepos + self.offset).coordinates

    @property
    def pos(self):
        return Point.from_coordinates(self.primitive.position)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, new_offset):
        self.primitive.position = ((self.pos - self._offset) + new_offset).coordinates
        self._offset = new_offset

    @property
    def layer(self):
        match self.primitive.group.order:
            case 0:
                return Layer.FRONT
            case 1:
                return Layer.FOREGROUND
            case 2:
                return Layer.MIDGROUND
            case 3:
                return Layer.BACKGROUND
            case 4:
                return Layer.BACK

    @layer.setter
    def layer(self, layer):
        match layer:
            case Layer.FRONT:
                self.primitive.group = shape_front
            case Layer.FOREGROUND:
                self.primitive.group = shape_foreground
            case Layer.MIDGROUND:
                self.primitive.group = shape_midground
            case Layer.BACKGROUND:
                self.primitive.group = shape_background
            case Layer.BACK:
                self.primitive.group = shape_back
            case _:
                raise ValueError(f'Unexpected layer, {layer}')


class Circle(Shape):
    def __init__(self, ox, oy, color, radius):
        shape = pyglet.shapes.Circle(x=ox,
                                     y=oy,
                                     radius=radius,
                                     color=color,
                                     batch=shape_batch,
                                     group=shape_background)
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


class Rectangle(Shape):
    def __init__(self, ox, oy, color, width, height):
        shape = pyglet.shapes.Rectangle(x=ox,
                                        y=oy,
                                        width=width,
                                        height=height,
                                        color=color,
                                        batch=shape_batch,
                                        group=shape_background)
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
