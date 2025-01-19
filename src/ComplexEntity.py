

from ComplexImage import ComplexImage
from GraphicalEntity import GraphicalEntity


class ComplexEntity(GraphicalEntity):
    def __init__(self, x, y, dx, dy):
        image = ComplexImage(x, y)
        super().__init__(x, y, dx, dy, image)
