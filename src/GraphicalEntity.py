
from copy import copy
from functools import wraps

from Entity import Entity
from Geometry import Point, Vector

# todo:
# Performance test
#   self.image.pos.x = self.pos.x / self.image.pos.y = self.pos.y
#   self.image.pos = copy(self.pos)
# move base graphical entity to Entity


def static_update_function(f):
    '''Enforce update function assumption that object will not move.'''
    @wraps(f)
    def wrapper(self, *args, **kw):
        old_pos = copy(self.pos)
        result = f(self, *args, **kw)
        # Assert no change to position of entity
        assert self.pos == old_pos
        return result
    return wrapper


class GraphicalEntity(Entity):
    def __init__(self, x, y, dx, dy, image, static=False):
        super().__init__()
        self._pos = Point(x, y)
        self.vel = Vector(dx, dy)
        self.static = static

        self.image = image
        self.repr.append(self.image)

    def __str__(self):
        return f'{type(self).__name__}(x={self.pos.x},y={self.pos.y})'

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self.image.update_position(pos)

    @static_update_function
    def _update(self, dt):
        '''Apply update logic. Does not move or draw the entity.'''
        super()._update(dt)

    def _move(self, dt):
        '''Apply simulation movement logic.'''
        self.pos += self.vel * dt

    def move(self, dt):
        if self.enable and self.alive and not self.static:
            self._move(dt)
