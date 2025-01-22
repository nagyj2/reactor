
from util import Settings

from .image_complex import ComplexImage
from .shapes import Layer, Rectangle


class ScreenGrid(ComplexImage):
    def __init__(self, bx, by, split_x, split_y, thickness, color):
        assert split_x > 0, 'There must be 1 or more physics sectors'
        assert split_y > 0, 'There must be 1 or more physics sectors'

        self.split_x = split_x  # required for construction
        self.split_y = split_y
        self._thickness = thickness
        self._color = color

        super().__init__(bx, by)

    def _construct(self):
        for x in range(0, Settings.WIDTH, Settings.WIDTH // self.split_x):
            rect = Rectangle(x - self.thickness/2, 0, self.color, self.thickness, Settings.HEIGHT)
            rect.layer = Layer.BACK
            self[f'rect-x={x}'] = rect

        for y in range(0, Settings.HEIGHT, Settings.HEIGHT // self.split_y):
            rect = Rectangle(0, y - self.thickness/2, self.color, Settings.WIDTH, self.thickness)
            rect.layer = Layer.BACK
            self[f'rect-y={y}'] = rect

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        for name, shape in self._shapes:
            if 'rect-x' in name:
                shape.width = thickness
            else:
                shape.height = thickness

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        for shape in self.shapes:
            shape.color = color
