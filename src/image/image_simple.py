
from geometry import Point

from .image import Image


class SimpleImage(Image):
    '''Convinience class for images with 1 shape. Shortcuts several operations on Image.'''
    _base_name = 'base'

    def __init__(self, bx, by, shape):
        super().__init__(bx, by)
        shape.move_to(Point(bx, by))
        self[self._base_name] = shape

    def __getitem__(self, name):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot retreive additional shape \'{name}\'')
        return super().__getitem__(name)

    def __setitem__(self, name, shape):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot assign additional shape \'{name}\'')
        return super().__setitem__(name, shape)

    def __delitem__(self, name):
        if name != self._base_name:
            raise IndexError(f'{type(self).__name__} cannot retreive additional shape \'{name}\'')
        raise AttributeError(f'{type(self).__name__} cannot have only shape removed')

    @property
    def color(self):
        return self[self._base_name].color

    @color.setter
    def color(self, color):
        self[self._base_name].color = color

    @property
    def offset(self):
        return self[self._base_name].offset

    @offset.setter
    def offset(self, offset):
        self[self._base_name].offset = offset

    @property
    def layer(self):
        return self[self._base_name].layer

    @layer.setter
    def layer(self, layer):
        self[self._base_name].layer = layer
