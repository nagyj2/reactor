
from Shapes import Layer
from SimpleGraphicalEntity import RectangleEntity
from Thermal import Thermal

# todo:
# add moderator ability
# add absorption trigger ability

BABY_BLUE = (137, 207, 240, 64)


class Water(RectangleEntity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, 0, 0, BABY_BLUE, w, h, static=True)
        self.thermal = Thermal(50, Water, 50)
        self.repr.append(self.thermal)

        self.image.layer = Layer.BACKGROUND

    def _update(self, dt):
        self.image.color = tuple(map(lambda c: int(min(max(c * self.thermal.T/50, 0), 255)), BABY_BLUE))
        self.thermal.dissipate(dt)
