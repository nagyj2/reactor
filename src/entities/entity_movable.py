
from image import Layer

from .component_controller import BasicController
from .component_thermal import Thermal
from .entity_simple_shapes import CircleEntity

GREEN = (0, 255, 0, 128)


class Moveable(CircleEntity):
    def __init__(self, x, y, speed, radius, window, keymapping):
        super().__init__(x, y, 0, 0, GREEN, radius)
        self.controller = BasicController(self, speed, window, keymapping)
        self.thermal = Thermal(75, Moveable)
        self.repr.extend([self.controller, self.thermal])

        self.image.layer = Layer.FRONT
