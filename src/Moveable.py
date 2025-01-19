
from Controller import BasicController
from Shapes import Layer
from SimpleGraphicalEntity import CircleEntity

GREEN = (0, 255, 0, 128)


class Moveable(CircleEntity):
    def __init__(self, x, y, speed, radius, window, keymapping):
        super().__init__(x, y, 0, 0, GREEN, radius)
        self.controller = BasicController(self, speed, window, keymapping)
        self.repr.append(self.controller,)

        self.image.layer = Layer.FRONT
