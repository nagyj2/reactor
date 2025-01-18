
from GraphicalEntity import RectangleEntity
from Shapes import Layer

# todo:
# add moderator ability
# add absorption trigger ability

BABY_BLUE = (137, 207, 240, 64)


class Water(RectangleEntity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, 0, 0, BABY_BLUE, w, h, static=True)

        self.image.set_layer(Layer.BACKGROUND)
