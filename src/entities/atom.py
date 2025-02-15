
from image import Layer

from .component_emitter import Radioactivity
from .entity_simple_shapes import CircleEntity

# todo:
# radioactivity
# depleated state

RED = (255, 0, 0, 255)


class Atom(CircleEntity):
    def __init__(self, x, y, dx, dy, radius, emit_num, emit_chance, emit_particle, entity_space):
        super().__init__(x, y, dx, dy, RED, radius, static=True)
        self.radioactivity = Radioactivity(self.pos, emit_particle, emit_num, 100, entity_space, emit_chance)
        self.repr.append(self.radioactivity)

        self.image.layer = Layer.MIDGROUND
