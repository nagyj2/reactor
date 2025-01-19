from copy import deepcopy

import pytest

from Geometry import Point, Vector
from Image import (CircleImage, ComplexImage, Image, PointImage,
                   RectangleImage, SimpleImage)
from Settings import init_settings
from Shapes import Circle, Layer, Rectangle

# todo:


init_settings(default=True)

params_shapes = [
    Circle,
    Rectangle,
]


def init_shape(shape):
    if shape is Circle:
        return Circle(0, 0, (255, 128, 64), 5)
    elif shape is Rectangle:
        return Rectangle(0, 0, (255, 128, 64), 3, 5)
    assert False, 'Invalid shape'


def test_image_creation():
    i = Image(0, 0)
    assert i.basepos == Point(0, 0)
    assert len(i.shapes) == 0


@pytest.mark.parametrize('shape_class', params_shapes)
def test_image_set_get_del(shape_class):
    s1 = init_shape(shape_class)
    i = Image(0, 0)
    i['shape'] = s1
    assert len(i.shapes) == 1
    assert s1 in i
    assert i['shape'] == s1
    del i['shape']
    assert len(i.shapes) == 0


@pytest.mark.parametrize('shape_class', params_shapes)
def test_image_set_get_del_many(shape_class):
    s1 = init_shape(shape_class)
    s2 = deepcopy(s1)
    s2.offset.x += 1  # make different so s1 != s2
    assert s1 != s2
    i = Image(0, 0)
    assert s1 is not None
    assert s2 is not None
    i['shape1'] = s1
    i['shape2'] = s2
    assert len(i.shapes) == 2
    assert s1 in i
    assert s2 in i
    assert i['shape1'] == s1
    assert i['shape2'] == s2

    del i['shape1']
    assert len(i.shapes) == 1
    assert s1 not in i
    assert s2 in i
    assert i['shape2'] == s2


@pytest.mark.parametrize('shape_class', params_shapes)
def test_image_set_layer(shape_class):
    s1 = init_shape(shape_class)
    s2 = deepcopy(s1)
    layer = Layer.BACK
    i = Image(0, 0)
    i['shape1'] = s1
    i['shape2'] = s2
    i.set_layer(layer)
    assert i['shape1'].primitive.group.order == int(layer)
    assert i['shape2'].primitive.group.order == int(layer)


@pytest.mark.parametrize('shape_class', params_shapes)
def test_image_draw(shape_class):
    shape1 = init_shape(shape_class)
    i = Image(0, 0)
    i['shape1'] = shape1
    assert i.basepos.coordinates == shape1.primitive.position

    dx, dy = 1, 1
    i.basepos += Vector(dx, dy)
    i.draw()
    assert i.basepos.coordinates == shape1.primitive.position


@pytest.mark.parametrize('shape_class', params_shapes)
def test_simpleimage_creation(shape_class):
    shape = init_shape(shape_class)
    x, y = 0, 0
    i = SimpleImage(x, y, shape)
    assert i.basepos.coordinates == (x, y)
    assert len(i.shapes) == 1
    assert i.color == shape.color


@pytest.mark.parametrize('shape_class', params_shapes)
def test_simpleimage_set_get_del(shape_class):
    shape = init_shape(shape_class)
    i = SimpleImage(0, 0, shape)
    # i['base'] = shape
    assert len(i.shapes) == 1
    assert shape in i
    assert i['base'] == shape

    with pytest.raises(AttributeError):
        del i['base']
        assert len(i.shapes) == 0


@pytest.mark.parametrize('shape_class', params_shapes)
def test_simpleimage_set_get_del_invalid(shape_class):
    shape = init_shape(shape_class)
    i = SimpleImage(0, 0, shape)

    with pytest.raises(IndexError):
        del i['_not_available']
    with pytest.raises(IndexError):
        i['_not_available'] = shape
    with pytest.raises(IndexError):
        i['_not_available']


@pytest.mark.parametrize('shape_class', params_shapes)
def test_simpleimage_set_get_color(shape_class):
    shape = init_shape(shape_class)
    i = SimpleImage(0, 0, shape)

    for color in ((255, 0, 0, 255), (128, 64, 255, 255)):
        i.color = color
        assert i.color == color
        assert i['base'].primitive.color == color


def test_pointimage_set_get_radius():
    i = PointImage(0, 0, (255, 255, 255), 5)

    for radius in (-10, 0, 10):
        i.radius = radius
        i.draw()  # fix to not need - pipe call
        assert i.radius == radius == i['base'].primitive.radius


def test_circleimage_set_get_radius():
    i = CircleImage(0, 0, (255, 255, 255), 5)

    for radius in (-10, 0, 10):
        i.radius = radius
        i.draw()  # fix to not need - pipe call
        assert i.radius == radius == i['base'].primitive.radius


def test_rectangleimage_set_get_radius():
    i = RectangleImage(0, 0, (255, 255, 255), 5, 5)

    for w, h in ((-10, 10), (0, 5), (10, 0)):
        i.width, i.height = w, h
        i.draw()  # fix to not need - pipe call
        assert i.width == w == i['base'].primitive.width
        assert i.height == h == i['base'].primitive.height


def test_compleximage_creation():
    i = ComplexImage(0, 0)
    assert i.basepos == Point(0, 0)
    assert len(i.shapes) == 0
