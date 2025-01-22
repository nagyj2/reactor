
from util import Physics

from .graphical_entity import GraphicalEntity


class SimpleGraphicalEntity(GraphicalEntity):
    def __init__(self, x, y, dx, dy, image, static=False):
        super().__init__(x, y, dx, dy, image, static)
        self.physics = Physics.PhysicsType.Simple

    @property
    def color(self):
        return self.image.color

    @color.setter
    def color(self, color):
        self.image.color = color
