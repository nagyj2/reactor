
from Controller import BasicController
from Shapes import Layer
from SimpleGraphicalEntity import CircleEntity
from Thermal import Thermal

GREEN = (0, 255, 0, 128)


class Moveable(CircleEntity):
    def __init__(self, x, y, speed, radius, window, keymapping):
        super().__init__(x, y, 0, 0, GREEN, radius)
        self.controller = BasicController(self, speed, window, keymapping)
        self.thermal = Thermal(75, Moveable)
        self.repr.extend([self.controller, self.thermal])

        self.image.layer = Layer.FRONT
