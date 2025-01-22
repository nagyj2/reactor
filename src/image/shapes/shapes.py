
import enum
from copy import deepcopy

from geometry import Point, Vector

from .constants import (shape_back, shape_background, shape_batch,
                        shape_foreground, shape_front, shape_midground)

# todo:
# on __del__, remove from batch
# instea dof storing colour at each instance, use properties to bypass layers

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
        self.primitive.batch = shape_batch
        self.primitive.group = shape_background

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
