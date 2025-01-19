import copy
import re
import sys

import pytest

from Geometry import EPSILON, Point, Vector

# todo:
# get dependencies working
#   for parameterized tests, you need to autogenerate test names for each test
#   pytest-dependency/readthedocs.io/en/stable/advanced.html under 'Depend on all
#   instances of a parameterized test at once'
# make useful param categories
#   cardinal and diagonal directions
#   any 'golden' pairs for interesting behaviour
#   on the origin
#   within epsilon
#   just outside epsilon
#   maximum float
#   separate into single coord pairs and double coord pairs

params_copy = [
    (Point(1, 2), 1, 0),
    (Point(1, 2), 0, 1),
    (Point(1, 2), 0.5, 0),
    (Point(1, 2), 0, EPSILON * 10),
]

# 2 vector coordinates, none are the same
params_coord_math_auto_verify = [
    (1, 1, 1, -1),
    (1, 0, -1, 0),
    (1, 0, 1, -.2),
    (1, 0, -1, 0),
    (1, 0, 1.3, -2.5),
    (-1, 2.0, -1, 2.1),
    (0, 0, 0, EPSILON * 10),
    (4.3, 1/3, 4.4, 0.3333333333333),
]

params_math_invalid_types = [
    ('w',),
    (1,),
    (1.0,),
    (True,),
    (object(),),
]


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify)
def test_point_correct_value(x1, y1, x2, y2):
    p1 = Point(x1, y1)
    assert p1.x == x1
    assert p1.y == y1
    p2 = Point(x2, y2)
    assert p2.x == x2
    assert p2.y == y2


@pytest.mark.parametrize('tx,ty,ex,ey,et', [
    (1, 2, 1, 2.0, float),
    (-1, -2, -1.0, -2.0, float),
    (1, -2, 1.0, -2.0, float),
    (-1, 2, -1.0, 2.0, float),
    (sys.float_info.min, sys.float_info.min, float(sys.float_info.min), float(sys.float_info.min), float),
    ('1', '-1', 1.0, -1.0, float),
    ('23', '0.43', 23, 0.43, float),
    ('0', '-0', 0.0, 0.0, float),
])
def test_point_valid_conv(tx, ty, ex, ey, et):
    p1 = Point(tx, ty)
    assert p1.x == ex
    assert p1.y == ey
    assert type(p1.x) is type(p1.y) is et


@pytest.mark.parametrize('x,y', [
    ('w', 0.0), (0.0, 'w'),
    (True, 0.0,), (0.0, True),
    ('1.0s', 0.0), (0.0, '1.0s'),
    ('1.0', 0.0), (0.0, '1.0'),
    (None, 0.0), (0.0, None),
])
def test_point_invalid_conv(x, y):
    with pytest.raises(TypeError, match=r'\'\w+\' must be a number$'):
        Point(x, y)


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify)
def test_point_str(x1, y1, x2, y2):
    assert str(Point(x1, y1)) == f'({round(float(x1), 2)}, {round(float(y1), 2)})'
    assert str(Point(x2, y2)) == f'({round(float(x2), 2)}, {round(float(y2), 2)})'


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify)
def test_point_eq(x1, y1, x2, y2):
    assert Point(x1, y1) == Point(x1, y1)
    assert Point(x2, y2) == Point(x2, y2)


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify)
def test_point_ne(x1, y1, x2, y2):
    assert Point(x1, y1) != Point(x2, y2)


@pytest.mark.parametrize('x,y,ox,oy', params_coord_math_auto_verify)
def test_point_copy(x, y, ox, oy):
    p1 = Point(x, y)
    p2 = copy.copy(p1)
    assert p1 == p2
    p1.x = p1.x + ox
    p1.y = p1.y + oy
    assert p1 != p2


@pytest.mark.parametrize('x,y,ox,oy', params_coord_math_auto_verify)
def test_point_deepcopy(x, y, ox, oy):
    p1 = Point(x, y)
    p2 = copy.deepcopy(p1)
    assert p1 == p2
    p1.x = p1.x + ox
    p1.y = p1.y + oy
    assert p1 != p2


@pytest.mark.parametrize('x,y,dx,dy', params_coord_math_auto_verify)
def test_point_vector_add(x, y, dx, dy):
    p1 = Point(x, y)
    v1 = Vector(dx, dy)
    assert (p1 + v1).x == x + dx
    assert (p1 + v1).y == y + dy
    assert (p1 + v1 + v1).x == x + dx + dx
    assert (p1 + v1 + v1).y == y + dy + dy


@pytest.mark.parametrize('o2', params_math_invalid_types)
def test_point_vector_add_invalid(o2):
    p1 = Point(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'unsupported operand type(s) for +: \'{type(p1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        p1 = p1 + o2


@pytest.mark.parametrize('x,y,dx,dy', params_coord_math_auto_verify)
def test_point_vector_sub(x, y, dx, dy):
    p1 = Point(x, y)
    v1 = Vector(dx, dy)
    assert (p1 - v1).x == x - dx
    assert (p1 - v1).y == y - dy
    assert (p1 - v1 - v1).x == x - dx - dx
    assert (p1 - v1 - v1).y == y - dy - dy


@pytest.mark.parametrize('o2', params_math_invalid_types)
def test_point_vector_sub_invalid(o2):
    p1 = Point(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'unsupported operand type(s) for -: \'{type(p1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        p1 = p1 - o2


@pytest.mark.parametrize('x,y,dx,dy', params_coord_math_auto_verify)
def test_point_vector_iadd(x, y, dx, dy):
    p1 = Point(x, y)
    p1_copy = copy.copy(p1)
    v1 = Vector(dx, dy)
    p1 += v1
    assert p1 == p1_copy + v1
    p1 += v1
    assert p1 == p1_copy + v1 + v1


@pytest.mark.parametrize('x,y,dx,dy', params_coord_math_auto_verify)
def test_point_vector_isub(x, y, dx, dy):
    p1 = Point(x, y)
    p1_copy = copy.copy(p1)
    v1 = Vector(dx, dy)
    p1 -= v1
    assert p1 == p1_copy - v1
    p1 -= v1
    assert p1 == p1_copy - v1 - v1


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify)
def test_point_coordinates_get(x1, y1, x2, y2):
    assert Point(x1, y1).coordinates == Point(x1, y1).coordinates
    assert Point(x2, y2).coordinates == Point(x2, y2).coordinates


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify)
def test_point_coordinates_set(x1, y1, x2, y2):
    for x_y in ((x1, y1), (x2, y2)):
        x, y = x_y[0], x_y[1]
        p1 = Point(0, 0)
        p1.coordinates = (x, y)
        assert p1.coordinates == (x, y)
        assert p1.coordinates == Point(x, y).coordinates


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify)
def test_point_from_origin(x1, y1, x2, y2):
    assert Point.from_origin(Vector(x1, y1)) == Point(x1, y1)
    assert Point.from_origin(Vector(x2, y2)) == Point(x2, y2)
