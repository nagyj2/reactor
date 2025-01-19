from copy import copy, deepcopy

import pyglet
import pytest

from Geometry import Vector
from Settings import init_settings
from Shapes import (Circle, Layer, Rectangle, Shape, shape_back,
                    shape_background, shape_foreground, shape_front,
                    shape_midground)

# todo:
# add parameterization

init_settings(default=True)


def create_pyglet_shape_sample(x, y, color):
    return pyglet.shapes.Circle(x=float(x),
                                y=float(y),
                                radius=1,
                                color=color,
                                group=shape_background)


def create_shape_sample(ox, oy, color):
    primitive = create_pyglet_shape_sample(ox, oy, color)
    return Shape(ox, oy, primitive, color)


def validate_shape(shape, ex, ey, eox, eoy, ecolor):
    assert shape.offset.x == eox
    assert shape.primitive.x == ex
    assert shape.offset.y == eoy
    assert shape.primitive.y == ey
    assert shape.color == ecolor == shape.primitive.color


def test_shape_value():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    s1 = create_shape_sample(ox, oy, color)
    validate_shape(s1, ox, oy, ox, oy, color)

    ox, oy = '-1', '-2.0'
    validate_shape(create_shape_sample(ox, oy, color), float(ox), float(oy), float(ox), float(oy), color)


@pytest.mark.dependency()
def test_shape_eq():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    s1 = create_shape_sample(ox, oy, color)
    s2 = create_shape_sample(ox, oy, color)
    assert s1 == s2
    s2 = create_shape_sample(ox+1, oy, color)
    assert not (s1 == s2)
    s2 = create_shape_sample(ox, oy-1, color)
    assert not (s1 == s2)
    s2 = create_shape_sample(ox, oy, (255, 255, 255, 255))
    assert not (s1 == s2)
    s2 = create_shape_sample(ox+1, oy+1, color)
    assert not (s1 == s2)

    s2 = create_shape_sample(ox, oy, color)
    s2.primitive.x = s2.primitive.x + 1
    assert not (s1 == s2)
    s2 = create_shape_sample(ox, oy, color)
    s2.primitive.y = s2.primitive.y + 1
    assert not (s1 == s2)
    s2 = create_shape_sample(ox, oy, color)
    s2.primitive.color = (255, 255, 255)
    assert not (s1 == s2)


@pytest.mark.dependency()
def test_shape_ne():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    s1 = create_shape_sample(ox, oy, color)
    s2 = create_shape_sample(ox, oy, color)
    assert not (s1 != s2)
    s2 = create_shape_sample(ox+1, oy, color)
    assert s1 != s2
    s2 = create_shape_sample(ox+1, oy+1, color)
    assert s1 != s2
    s2 = create_shape_sample(ox, oy+1, color)
    assert s1 != s2
    s2 = create_shape_sample(ox+1, oy+1, (255, 255, 255, 255))
    assert s1 != s2

    s2 = create_shape_sample(ox, oy, color)
    s2.primitive.x = s2.primitive.x + 1
    assert s1 != s2
    s2 = create_shape_sample(ox, oy, color)
    s2.primitive.y = s2.primitive.y + 1
    assert s1 != s2
    s2 = create_shape_sample(ox, oy, color)
    s2.primitive.color = (255, 255, 255)
    assert s1 != s2


@pytest.mark.dependency(depends=['test_shape_eq', 'test_shape_ne'])
def test_shape_copy():
    s1 = create_shape_sample(0, 0, (255, 128, 64, 32))
    s2 = copy(s1)
    assert s1 == s2

    color = (255, 255, 255, 255)
    s1.primitive.color = color
    assert s1 == s2
    s1.color = color
    assert s1 != s2


@pytest.mark.dependency(depends=['test_shape_eq', 'test_shape_ne'])
def test_shape_deepcopy():
    s1 = create_shape_sample(0, 0, (255, 128, 64, 32))
    s2 = deepcopy(s1)
    assert s1 == s2

    color = (255, 255, 255, 255)
    s1.primitive.color = color
    assert s1 != s2
    s1.color = color
    assert s1 != s2


def test_shape_draw():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    s1 = create_shape_sample(ox, oy, color)

    s1.draw()  # properties should be static
    validate_shape(s1, ox, oy, ox, oy, color)

    s1.offset += Vector(1, -1)
    s1.color = (255, 255, 255, 22)
    s1.draw()  # see if properties update
    validate_shape(s1, ox+1, oy-1, ox+1, oy-1, (255, 255, 255, 22))

    # 2 back-to-back draw() calls will not happen without x,y being reset by Image
    # results in constant offset but different primitive position
    s1.draw()
    validate_shape(s1, ox+2, oy-2, ox+1, oy-1, (255, 255, 255, 22))


def test_shape_layer():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    s1 = create_shape_sample(ox, oy, color)
    s1.set_layer(Layer.FRONT)
    assert s1.primitive.group == shape_front
    s1.set_layer(Layer.FOREGROUND)
    assert s1.primitive.group == shape_foreground
    s1.set_layer(Layer.MIDGROUND)
    assert s1.primitive.group == shape_midground
    s1.set_layer(Layer.BACKGROUND)
    assert s1.primitive.group == shape_background
    s1.set_layer(Layer.BACK)
    assert s1.primitive.group == shape_back


def validate_circle(circ, ex, ey, eox, eoy, ecolor, eradius):
    assert circ.offset.x == eox
    assert circ.primitive.x == ex
    assert circ.offset.y == eoy
    assert circ.primitive.y == ey
    assert circ.color == ecolor == circ.primitive.color
    assert circ.radius == eradius == circ.primitive.radius


def test_circle_value():
    ox, oy = 0, 0
    color = (255, 128, 64, 32)
    radius = 5
    c1 = Circle(ox, oy, color, radius)
    validate_circle(c1, ox, oy, ox, oy, color, radius)

    radius = -3
    validate_circle(Circle(ox, oy, color, radius), ox, oy, ox, oy, color, radius)


@pytest.mark.dependency()
def test_circle_eq():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    radius = 3
    c1 = Circle(ox, oy, color, radius)
    c2 = Circle(ox, oy, color, radius)
    assert c1 == c2
    c2 = Circle(ox+1, oy, color, radius)
    assert not (c1 == c2)
    c2 = Circle(ox, oy-1, color, radius)
    assert not (c1 == c2)
    c2 = Circle(ox, oy, (255, 255, 255, 255), radius)
    assert not (c1 == c2)
    c2 = Circle(ox+1, oy+1, color, radius)
    assert not (c1 == c2)
    c2 = Circle(ox, oy, color, radius+1)
    assert not (c1 == c2)

    c1 = Circle(ox, oy, color, radius)
    c2.primitive.x = c2.primitive.x + 1
    assert not (c1 == c2)
    c1 = Circle(ox, oy, color, radius)
    c2.primitive.y = c2.primitive.y + 1
    assert not (c1 == c2)
    c1 = Circle(ox, oy, color, radius)
    c2.primitive.color = (255, 255, 255)
    assert not (c1 == c2)
    c1 = Circle(ox, oy, color, radius)
    c2.primitive.radius = radius + 1
    assert not (c1 == c2)


@pytest.mark.dependency()
def test_circle_ne():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    radius = 3
    c1 = Circle(ox, oy, color, radius)
    c2 = Circle(ox, oy, color, radius)
    assert not (c1 != c2)
    c2 = Circle(ox+1, oy, color, radius)
    assert c1 != c2
    c2 = Circle(ox+1, oy+1, color, radius)
    assert c1 != c2
    c2 = Circle(ox, oy+1, color, radius)
    assert c1 != c2
    c2 = Circle(ox+1, oy+1, (255, 255, 255, 255), radius)
    assert c1 != c2
    c2 = Circle(ox, oy, color, radius+1)
    assert c1 != c2

    c2 = Circle(ox, oy, color, radius)
    c2.primitive.x = c2.primitive.x + 1
    assert not (c1 == c2)
    c2 = Circle(ox, oy, color, radius)
    c2.primitive.y = c2.primitive.y + 1
    assert not (c1 == c2)
    c2 = Circle(ox, oy, color, radius)
    c2.primitive.color = (255, 255, 255)
    assert not (c1 == c2)
    c2 = Circle(ox, oy, color, radius)
    c2.primitive.radius = radius + 1
    assert not (c1 == c2)


@pytest.mark.dependency(depends=['test_circle_eq', 'test_circle_ne'])
def test_circle_copy():
    c1 = Circle(0, 0, (255, 128, 64, 32), 5)
    c2 = copy(c1)
    assert c1 == c2

    color = (255, 255, 255, 255)
    c1.primitive.color = color
    assert c1 == c2
    c1.color = color
    assert c1 != c2


@pytest.mark.dependency(depends=['test_circle_eq', 'test_circle_ne'])
def test_circle_deepcopy():
    c1 = Circle(0, 0, (255, 128, 64, 32), 5)
    c2 = deepcopy(c1)
    assert c1 == c2

    color = (255, 255, 255, 255)
    c1.primitive.color = color
    assert c1 != c2
    c1.color = color
    assert c1 != c2


def test_circle_draw():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    radius = 10
    c1 = Circle(ox, oy, color, radius)

    c1.draw()  # properties should be static
    validate_circle(c1, ox, oy, ox, oy, color, radius)

    c1.offset += Vector(1, -1)
    c1.color = (255, 255, 255, 22)
    c1.radius = 7
    c1.draw()  # see if properties update
    validate_circle(c1, ox+1, oy-1, ox+1, oy-1, (255, 255, 255, 22), 7)

    # 2 back-to-back draw() calls will not happen without x,y being reset by Image
    # results in constant offset but different primitive position
    c1.draw()
    validate_circle(c1, ox+2, oy-2, ox+1, oy-1, (255, 255, 255, 22), 7)


def test_circle_layer():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    radius = 10
    c1 = Circle(ox, oy, color, radius)
    c1.set_layer(Layer.FRONT)
    assert c1.primitive.group == shape_front
    c1.set_layer(Layer.FOREGROUND)
    assert c1.primitive.group == shape_foreground
    c1.set_layer(Layer.MIDGROUND)
    assert c1.primitive.group == shape_midground
    c1.set_layer(Layer.BACKGROUND)
    assert c1.primitive.group == shape_background
    c1.set_layer(Layer.BACK)
    assert c1.primitive.group == shape_back


def validate_rectangle(rect, ex, ey, eox, eoy, ecolor, ewidth, eheight):
    assert rect.offset.x == eox
    assert rect.primitive.x == ex
    assert rect.offset.y == eoy
    assert rect.primitive.y == ey
    assert rect.color == ecolor == rect.primitive.color
    assert rect.width == ewidth == rect.primitive.width
    assert rect.height == eheight == rect.primitive.height


def test_rectangle_value():
    ox, oy = 0, 0
    color = (255, 128, 64, 32)
    w, h = 20, 10
    r1 = Rectangle(ox, oy, color, w, h)
    validate_rectangle(r1, ox, oy, ox, oy, color, w, h)

    r1 = Rectangle(ox, oy, color, -1, 0)
    validate_rectangle(r1, ox, oy, ox, oy, color, -1, 0)


@pytest.mark.dependency()
def test_rectangle_eq():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    w, h = -3, 6
    r1 = Rectangle(ox, oy, color, w, h)
    r2 = Rectangle(ox, oy, color, w, h)
    assert r1 == r2
    r2 = Rectangle(ox+1, oy, color, w, h)
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy-1, color, w, h)
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy, (255, 255, 255, 255), w, h)
    assert not (r1 == r2)
    r2 = Rectangle(ox+1, oy+1, color, w, h)
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy, color, w+1, h)
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy, color, w, h+1)
    assert not (r1 == r2)

    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.x = r2.primitive.x + 1
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.y = r2.primitive.y + 1
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.color = (255, 255, 255)
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.width = r2.primitive.width + 1
    assert not (r1 == r2)
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.height = r2.primitive.height + 1
    assert not (r1 == r2)


@pytest.mark.dependency()
def test_rectangle_ne():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    w, h = -3, 6
    r1 = Rectangle(ox, oy, color, w, h)
    r2 = Rectangle(ox, oy, color, w, h)
    assert not (r1 != r2)
    r2 = Rectangle(ox+1, oy, color, w, h)
    assert r1 != r2
    r2 = Rectangle(ox+1, oy+1, color, w, h)
    assert r1 != r2
    r2 = Rectangle(ox, oy+1, color, w, h)
    assert r1 != r2
    r2 = Rectangle(ox+1, oy+1, (255, 255, 255, 255), w, h)
    assert r1 != r2
    r2 = Rectangle(ox, oy, color, w+1, h)
    assert r1 != r2
    r2 = Rectangle(ox, oy, color, w, h+1)
    assert r1 != r2

    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.x = r2.primitive.x + 1
    assert r1 != r2
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.y = r2.primitive.y + 1
    assert r1 != r2
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.color = (255, 255, 255)
    assert r1 != r2
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.width = r2.primitive.width + 1
    assert r1 != r2
    r2 = Rectangle(ox, oy, color, w, h)
    r2.primitive.height = r2.primitive.height + 1
    assert r1 != r2


@pytest.mark.dependency(depends=['test_rectangle_eq', 'test_rectangle_ne'])
def test_rectangle_copy():
    x, y = 0, 0
    w, h = 1, 2
    color = (255, 128, 64, 32)
    r1 = Rectangle(x, y, color, w, h)
    r2 = copy(r1)
    assert r1 == r2

    color = (255, 255, 255, 255)
    r1.primitive.color = color
    assert r1 == r2
    r1.color = color
    assert r1 != r2


@pytest.mark.dependency(depends=['test_rectangle_eq', 'test_rectangle_ne'])
def test_rectangle_deepcopy():
    r1 = Rectangle(0, 0, (255, 128, 64, 32), 5, 6)
    r2 = deepcopy(r1)
    assert r1 == r2

    color = (255, 255, 255, 255)
    r1.primitive.color = color
    assert r1 != r2
    r1.color = color
    assert r1 != r2


def test_rectangle_draw():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    w, h = 5, -2
    r1 = Rectangle(ox, oy, color, w, h)

    r1.draw()  # properties should be static
    validate_rectangle(r1, ox, oy, ox, oy, color, w, h)

    r1.offset += Vector(1, -1)
    r1.color = (255, 255, 255, 22)
    r1.width = -2.5
    r1.height = 2.35
    r1.draw()  # see if properties update
    validate_rectangle(r1, ox+1, oy-1, ox+1, oy-1, (255, 255, 255, 22), -2.5, 2.35)

    # 2 back-to-back draw() calls will not happen without x,y being reset by Image
    # results in constant offset but different primitive position
    r1.draw()
    validate_rectangle(r1, ox+2, oy-2, ox+1, oy-1, (255, 255, 255, 22), -2.5, 2.35)


def test_rectangle_layer():
    ox, oy = 0, 0
    color = (255, 128, 64, 255)
    radius = 10
    r1 = Circle(ox, oy, color, radius)
    r1.set_layer(Layer.FRONT)
    assert r1.primitive.group == shape_front
    r1.set_layer(Layer.FOREGROUND)
    assert r1.primitive.group == shape_foreground
    r1.set_layer(Layer.MIDGROUND)
    assert r1.primitive.group == shape_midground
    r1.set_layer(Layer.BACKGROUND)
    assert r1.primitive.group == shape_background
    r1.set_layer(Layer.BACK)
    assert r1.primitive.group == shape_back
