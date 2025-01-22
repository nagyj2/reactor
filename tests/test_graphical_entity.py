
import math

import pytest

from entities import CircleEntity, PointEntity, RectangleEntity
from entities.graphical_entity import GraphicalEntity
from entities.graphical_entity_complex import ComplexGraphicalEntity
from entities.graphical_entity_simple import SimpleGraphicalEntity
from geometry import EPSILON, Point, Vector
from image import CircleImage
from image.image_complex import ComplexImage
from image.rectangle_image import RectangleImage

params_setup_args = [
    (1, 2, 3, 4, (255, 128, 64, 32), 5),
]

params_circle_args = [
    (1, 2, 3, 4, (255, 128, 64, 32), 5),
]

params_rect_args = [
    (1, 2, 3, 4, (255, 128, 64, 32), 5, 6),
]

# xPC1, yPC1, rPC1, xPC2, yPC2, rPC3
params_2_point_circle_args = [
    (1, 2, 5, 1, 2, 5),
    (1, 2, 5, 2, 3, 1),
    (1, 2, 3, 5, 5, 1),
]

# xR1, yR1, wR1, hR1,  xR2, yR2, wR2, hR2
params_2_rect_args = [
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 2, 5, 6, 1, 2, 3, 4),
    (1, 2, 1, 1, 2, 3, 1, 1),
    (1, 2, 1, 1, 3, 4, 1, 1),
]

# xP, yP, rP, xC, yC, rC, xR, yR, wR, hR
params_point_circle_rect_args = [
    (1, 2, 5, 1, 2, 5, 1, 1, 1, 1),
]


@pytest.mark.parametrize('x,y,dx,dy,c,r', params_setup_args)
def test_graphical_entity_creation(x, y, dx, dy, c, r):
    i = CircleImage(0, 0, c, r)
    static = False
    e = GraphicalEntity(x, y, dx, dy, i, static)

    assert e.pos == Point(x, y)
    assert e.vel == Vector(dx, dy)
    assert e.static == static
    assert e.image == i


@pytest.mark.parametrize('x,y,dx,dy,c,r', params_setup_args)
def test_graphical_entity_move(x, y, dx, dy, c, r):
    i = CircleImage(0, 0, c, r)
    static = False
    e = GraphicalEntity(x, y, dx, dy, i, static)

    assert e.pos == Point(x, y)
    e.move(1)
    assert e.pos == Point(x, y) + Vector(dx, dy)
    e.move(1)
    assert e.pos == Point(x, y) + Vector(dx, dy) * 2


@pytest.mark.parametrize('x,y,dx,dy,c,r', params_setup_args)
def test_simple_graphical_entity_creation(x, y, dx, dy, c, r):
    i = CircleImage(0, 0, c, r)
    static = False
    e = GraphicalEntity(x, y, dx, dy, i, static)

    assert e.pos == Point(x, y)
    assert e.vel == Vector(dx, dy)
    assert e.static == static
    assert e.image == i


@pytest.mark.parametrize('x,y,dx,dy,c,r', params_setup_args)
def test_simple_graphical_entity_accessors(x, y, dx, dy, c, r):
    i = CircleImage(0, 0, c, r)
    static = False
    e = SimpleGraphicalEntity(x, y, dx, dy, i, static)

    assert e.color == c


@pytest.mark.parametrize('x,y,dx,dy,c,r', params_setup_args)
def test_complex_graphical_entity_creation(x, y, dx, dy, c, r):
    static = False
    e = ComplexGraphicalEntity(x, y, dx, dy, static)

    assert e.pos == Point(x, y)
    assert e.vel == Vector(dx, dy)
    assert e.static == static
    assert type(e.image) is ComplexImage


@pytest.mark.parametrize('x,y,dx,dy,c,r', params_setup_args)
def test_point_entity_creation(x, y, dx, dy, c, r):
    static = False
    e = PointEntity(x, y, dx, dy, c, r, static)

    assert e.pos == Point(x, y)
    assert e.vel == Vector(dx, dy)
    assert e.static == static
    assert e.radius == r
    assert type(e.image) is CircleImage


@pytest.mark.parametrize('x1,y1,r1,x2,y2,r2', params_2_point_circle_args)
def test_point_point_entity_contains(x1, y1, r1, x2, y2, r2):
    truth = abs(x1-x2) < EPSILON and abs(y1-y2) < EPSILON
    e1 = PointEntity(x1, y1, 0, 0, (255, 255, 255), r1)
    e2 = PointEntity(x2, y2, 0, 0, (255, 255, 255), r2)

    assert (e1 in e2) == truth
    assert (e2 in e1) == truth


@pytest.mark.parametrize('x,y,dx,dy,c,r', params_setup_args)
def test_circle_entity_creation(x, y, dx, dy, c, r):
    static = False
    e = CircleEntity(x, y, dx, dy, c, r, static)

    assert e.pos == Point(x, y)
    assert e.vel == Vector(dx, dy)
    assert e.static == static
    assert e.radius == r
    assert type(e.image) is CircleImage


@pytest.mark.parametrize('x1,y1,r1,x2,y2,r2', params_2_point_circle_args)
def test_circle_circle_entity_contains(x1, y1, r1, x2, y2, r2):
    truth = math.dist((0, 0), (abs(x1-x2), abs(y1-y2))) <= r1 + r2
    e1 = CircleEntity(x1, y1, 0, 0, (255, 255, 255), r1)
    e2 = CircleEntity(x2, y2, 0, 0, (255, 255, 255), r2)

    assert (e1 in e2) == truth
    assert (e2 in e1) == truth


@pytest.mark.parametrize('x,y,dx,dy,c,w,h', params_rect_args)
def test_rectangle_entity_creation(x, y, dx, dy, c, w, h):
    static = False
    e = RectangleEntity(x, y, dx, dy, c, w, h, static)

    assert e.pos == Point(x, y)
    assert e.vel == Vector(dx, dy)
    assert e.static == static
    assert e.width == w
    assert e.height == h
    assert type(e.image) is RectangleImage


@pytest.mark.parametrize('x1,y1,w1,h1,x2,y2,w2,h2', params_2_rect_args)
def test_rectangle_rectangle_entity_contains(x1, y1, w1, h1, x2, y2, w2, h2):
    truth1 = x1+w1 < x2+w2 < x2 < x1 and y1+h1 < y2+h2 < y2 < y1
    truth2 = x2+w2 < x1+w1 < x1 < x2 and y2+h2 < y1+h1 < y1 < y2
    e1 = RectangleEntity(x1, y1, 0, 0, (255, 255, 255), w1, h1)
    e2 = RectangleEntity(x2, y2, 0, 0, (255, 255, 255), w2, h2)

    assert (e1 in e2) == truth1
    assert (e2 in e1) == truth2


def test_different_shape_entity_contains():
    assert False
