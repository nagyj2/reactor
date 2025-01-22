
import random
from typing import Callable

from geometry import Point, Vector
from image import Layer

from .entity import Entity
from .entity_simple_shapes import PointEntity

# todo:
# use __deepcopy__?
# correct get_per_frame_chance
# make nicer way add physics to particles
# implement custom particle emission


class Emitter(Entity):
    def __init__(self, x, y, emit_n, emit_vec_f, output_lst):
        super().__init__()
        self.origin = Point(x, y)
        self.output_lst = output_lst
        self.emit_n = emit_n
        self.emit_vec: Vector | Callable = emit_vec_f  # allow function for use with random emit directions

    def _create_particle(self):
        if callable(self.emit_vec):
            vel = self.emit_vec()
        else:
            vel = self.emit_vec
        particle = PointEntity(self.origin.x, self.origin.y,
                               vel.x, vel.y, (128, 128, 128), 3)
        particle.pos.coordinates = self.origin.coordinates
        particle.image.layer = Layer.FOREGROUND
        return particle

    def emit(self):
        for i in range(self.emit_n):
            particle = self._create_particle()
            self.output_lst.append(particle)


class ProbabilityEmitter(Emitter):
    def __init__(self, x, y, emit_n, emit_vec, output_lst, prob):
        super().__init__(x, y, emit_n, emit_vec, output_lst)
        self.probability = prob

    def update(self, dt):
        super()._update(dt)

        sample = random.random()
        if sample < self.probability:
            self.emit()


class TimeEmitter(Emitter):
    def __init__(self, x, y, emit_n, emit_vec, output_lst, timeframe):
        super().__init__(x, y, emit_n, emit_vec, output_lst)
        self.timeframe = timeframe
        self.passed_time = 0

    def update(self, dt):
        for _ in range(int((self.passed_time + dt) // self.timeframe)):
            self.emit()
        self.passed_time = (self.passed_time + dt) % self.timeframe


class Radioactivity(ProbabilityEmitter):
    def __init__(self, x, y, emit_n, emit_s, output_lst, probability):
        super().__init__(x, y, emit_n, lambda: Vector.from_polar_degrees(emit_s, random.random() * 360),
                         output_lst, probability)


class TestEmitter(TimeEmitter):
    def __init__(self, x, y, emit_n, entity_space, time):
        super().__init__(x, y, emit_n, lambda: Vector.from_polar_degrees(100, random.random() * 360),
                         entity_space, time)
