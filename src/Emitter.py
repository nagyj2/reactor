
import random
from typing import Callable

from Entity import Entity
from Geometry import Vector
from Neutron import Neutron
from Physics import GlobalPhysics as Physics
from Shapes import Layer

# todo:
# use __deepcopy__?
# correct get_per_frame_chance
# make nicer way add physics to particles


def get_per_frame_chance(chance_per_second, frames_per_second):
    return chance_per_second / frames_per_second


class Emitter(Entity):
    def __init__(self, origin, particle, emit_n, emit_vec_f, output_lst):
        super().__init__()
        self.origin = origin
        self.particle = particle
        self.output_lst = output_lst
        self.emit_n = emit_n
        self.emit_vec: Vector | Callable = emit_vec_f  # allow function for use with random emit directions

    def emit(self):
        for i in range(self.emit_n):
            # particle = deepcopy(self.particle)
            particle = Neutron(self.origin.x, self.origin.y, 1, 0, 2)

            particle.pos.coordinates = self.origin.coordinates
            particle.image.set_layer(Layer.FOREGROUND)
            Physics.add_to_sector(particle)

            if callable(self.emit_vec):
                particle.vel = self.emit_vec()
            else:
                particle.vel = self.emit_vec
            self.output_lst.append(particle)


class Emissive(Emitter):
    def __init__(self, origin, particle, emit_n, emit_vec_f, output_lst, chance):
        super().__init__(origin, particle, emit_n, emit_vec_f, output_lst)
        self.chance = chance

    def _update(self, dt):
        super()._update(dt)

        sample = random.random()
        if sample < self.chance:
            self.emit()


class Radioactivity(Emissive):
    def __init__(self, origin, particle, emit_n, emit_s, output_lst, chance):
        super().__init__(origin, particle, emit_n,
                         lambda: Vector.from_polar_degrees(emit_s, random.random() * 360), output_lst, chance)
