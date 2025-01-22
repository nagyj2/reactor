
from .image import Image


class ComplexImage(Image):
    def __init__(self, bx, by):
        super().__init__(bx, by)
        self._construct()

    def _construct(self):
        pass
