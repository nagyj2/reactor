
from image.image_complex import ComplexImage

from .graphical_entity import GraphicalEntity


class ComplexGraphicalEntity(GraphicalEntity):
    def __init__(self, x, y, dx, dy, static=False):
        image = ComplexImage(x, y)
        super().__init__(x, y, dx, dy, image, static)
