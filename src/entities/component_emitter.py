
import random
from typing import Callable

from geometry import Vector
from image import Layer
from util import Physics

from .entity import Entity
from .entity_simple_shapes import PointEntity

# todo:
# use __deepcopy__?
# correct get_per_frame_chance
# make nicer way add physics to particles


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
            particle = PointEntity(self.origin.x, self.origin.y,
                                   self.particle.vel.x, self.particle.vel.y, (128, 128, 128), 3)
            particle.pos.coordinates = self.origin.coordinates
            particle.image.layer = Layer.FOREGROUND
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


class TestEmitter(PointEntity):
    def __init__(self, x, y, radius, emit_rate, emit_num, entity_space):
        super().__init__(x, y, 0, 0, (255, 255, 0), radius, static=True)
        particle = PointEntity(x, y, 0, 0, (128, 128, 128), 3)
        self.emitter = Emitter(self.pos, particle, emit_num,
                               lambda: Vector.from_polar_degrees(100, random.random() * 360), entity_space)
        self.repr.append(self.emitter)

        self.image.layer = Layer.MIDGROUND
        self.time_passed = 0
        self.emit_rate = emit_rate

    def _update(self, dt):
        ot = self.time_passed
        self.time_passed = (self.time_passed + dt) % self.emit_rate
        if self.time_passed < ot:
            self.emitter.emit()
