
import enum
from copy import deepcopy

import pyglet

from Geometry import Coordinate, Vector

# todo:
# on __del__, remove from batch
# instea dof storing colour at each instance, use properties to bypass layers

shape_batch = pyglet.graphics.Batch()

shape_front = pyglet.graphics.Group(order=0)  # last to draw (top)
shape_foreground = pyglet.graphics.Group(order=1)
shape_midground = pyglet.graphics.Group(order=2)
shape_background = pyglet.graphics.Group(order=3)
shape_back = pyglet.graphics.Group(order=4)  # first to draw (bottom)

RED = (255, 0, 0)

# Mapping private attributes to public arguments in pyglet shapes
# Used for deepcopy. Only includes elements I am worried about
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
    def __init__(self, ox, oy, primitive, color):
        self.offset = Vector(ox, oy)
        self.primitive = primitive
        self.color = color

    def __iter__(self):
        return self.primitive  # return to use pyglet 2.0.8's `in` integration

    def __eq__(self, other):
        if isinstance(other, Shape):
            return self.offset == other.offset \
                and self.color == other.color \
                and self.primitive.__class__ == other.primitive.__class__ \
                and self.primitive.position == other.primitive.position \
                and self.primitive.color == other.primitive.color \
                and self.primitive.group == other.primitive.group
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

    def _draw(self):  # DIFFERENT FROM ENTITY `draw()`!
        self.primitive.x += self.offset.x  # apply offset
        self.primitive.y += self.offset.y
        self.primitive.color = self.color

    def draw(self):  # follow same structure as Entity but it is NOT THEIR `draw()`!
        self._draw()

    def set_layer(self, layer):
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

    @property
    def layer(self):
        return self.primitive.group


class Circle(Shape):
    radius = Coordinate()

    def __init__(self, ox, oy, color, radius):
        shape = pyglet.shapes.Circle(x=ox,
                                     y=oy,
                                     radius=radius,
                                     color=color,
                                     batch=shape_batch,
                                     group=shape_background)
        super().__init__(ox, oy, shape, color)

        self.radius = radius

    def __eq__(self, other):
        if isinstance(other, Circle):
            return super().__eq__(other) \
                and self.radius == other.radius \
                and self.primitive.radius == other.primitive.radius
        return False

    def _draw(self):  # DIFFERENT FROM ENTITY `draw()`!
        super()._draw()

        self.primitive.radius = self.radius


class Rectangle(Shape):
    width = Coordinate()
    height = Coordinate()

    def __init__(self, ox, oy, color, width, height):
        shape = pyglet.shapes.Rectangle(x=ox,
                                        y=oy,
                                        width=width,
                                        height=height,
                                        color=color,
                                        batch=shape_batch,
                                        group=shape_background)
        super().__init__(ox, oy, shape, color)

        self.width = width
        self.height = height

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return super().__eq__(other) \
                and self.width == other.width \
                and self.height == other.height \
                and self.primitive.width == other.primitive.width \
                and self.primitive.height == other.primitive.height
        return False

    def _draw(self):  # DIFFERENT FROM ENTITY `draw()`!
        super()._draw()

        self.primitive.width = self.width
        self.primitive.height = self.height
