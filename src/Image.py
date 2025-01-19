
from Entity import Entity

# todo:
# implement deepcopy
# change Image to be a graphical entity and then simple/complex shapes
#   come from it??
# improve API
#   pipe values up and down stack using properties
# add guards


class Image(Entity):
    def __init__(self, bx, by):
        super().__init__()

        self._named_shapes = {}

    def __getitem__(self, name):
        return self._named_shapes[name]

    def __setitem__(self, name, shape):
        assert shape is not None
        self._named_shapes[name] = shape

    def __delitem__(self, name):
        del self._named_shapes[name]

    def __len__(self):
        return len(self._named_shapes)  # number of shapes

    def __contains__(self, other):
        return other in self.shapes

    @property
    def shapes(self):
        return tuple(v for k, v in self._named_shapes.items())

    def set_layer(self, layer):
        for shape in self.shapes:
            shape.layer = layer

    def update_position(self, new_pos):
        for shape in self.shapes:
            # dv = Vector.from_positions(shape.pos, new_pos)
            shape.move_to(new_pos)
