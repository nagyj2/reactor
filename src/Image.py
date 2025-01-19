
from Entity import Entity
from Geometry import Point
from Shapes import Circle, Rectangle

# todo:
# implement deepcopy
# change Image to be a graphical entity and then simple/complex shapes
#   come from it??


class Image(Entity):
    def __init__(self, bx, by):
        super().__init__()

        self.basepos = Point(bx, by)
        self._named_shapes = {}

    def __getitem__(self, name):
        return self._named_shapes[name]

    def __setitem__(self, name, shape):
        shape.base = self
        self._named_shapes[name] = shape

    def __delitem__(self, name):
        del self._named_shapes[name]

    def __len__(self):
        return len(self._named_shapes)  # number of shapes

    @property
    def shapes(self):
        return tuple(iter(self._named_shapes.values()))

    def draw(self):
        '''Display update contained shapes. DIFFERENT FROM ENTITY `draw()`!'''
        self.basepos.coordinates = self.basepos.coordinates  # update self
        for name, shape in self._named_shapes.items():
            shape.primitive.position = self.basepos.coordinates  # update children to match self

            shape.draw()  # perform children offsets

    def set_layer(self, layer):
        for shape in self.shapes:
            shape.set_layer(layer)


class SimpleImage(Image):
    '''Convinience class for images with 1 shape. Shortcuts several operations on Image.'''
    _base_name = 'base'

    def __init__(self, bx, by, shape):
        super().__init__(bx, by)
        self[self._base_name] = shape

        self.color = shape.color

    def __getitem__(self, name):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot retreive additional shape \'{name}\'')
        return super().__getitem__(name)

    def __setitem__(self, name, shape):
        if name != self._base_name:
            raise AttributeError(f'{type(self).__name__} cannot assign additional shape \'{name}\'')
        return super().__setitem__(name, shape)

    def __delitem__(self, name):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot retreive additional shape \'{name}\'')
        raise AttributeError(f'{type(self).__name__} cannot have only shape removed')

    def set_layer(self, layer):
        self[self._base_name].set_layer(layer)

    def _draw(self):
        self[self._base_name].color = self.color

        super().draw()

    @property
    def color(self):
        return self[self._base_name].color

    @color.setter
    def color(self, color):
        self[self._base_name].color = color
        self.draw()  # propegate changes


class PointImage(SimpleImage):
    def __init__(self, bx, by, color, radius):
        shape = Circle(ox=0,  # ox and oy are image offsets
                       oy=0,
                       color=color,
                       radius=radius)
        super().__init__(bx, by, shape)

        self.radius = radius

    def _draw(self):
        self[self._base_name].radius = self.radius

        super()._draw()

    @property
    def radius(self):
        return self['base'].radius

    @radius.setter
    def radius(self, radius):
        self['base'].radius = radius


class CircleImage(SimpleImage):
    def __init__(self, bx, by, color, radius):
        shape = Circle(ox=0,
                       oy=0,
                       color=color,
                       radius=radius)
        super().__init__(bx, by, shape)

        self.radius = radius

    def _draw(self):
        self[self._base_name].radius = self.radius

        super()._draw()

    @property
    def radius(self):
        return self['base'].radius

    @radius.setter
    def radius(self, radius):
        self['base'].radius = radius


class RectangleImage(SimpleImage):
    def __init__(self, bx, by, color, width, height):
        shape = Rectangle(ox=0,
                          oy=0,
                          color=color,
                          width=width,
                          height=height)
        super().__init__(bx, by, shape)

        self.width = width
        self.height = height

    def _draw(self):
        self[self._base_name].width = self.width
        self[self._base_name].height = self.height

        super()._draw()

    @property
    def width(self):
        return self['base'].width

    @width.setter
    def width(self, width):
        self['base'].width = width

    @property
    def height(self):
        return self['base'].height

    @height.setter
    def height(self, height):
        self['base'].height = height


class ComplexImage(Image):
    def __init__(self, bx, by):
        super().__init__(bx, by)
