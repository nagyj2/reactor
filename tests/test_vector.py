import copy
import math
import re
import sys

import pytest

from geometry import EPSILON, Point, Vector

params_coord_w_offset = [
    (1, 2, 1, 0),
    (1, 2, 0, 1),
    (1, 2, 0.5, 0),
    (1, 2, 0, EPSILON * 10),
]

# 2 vector coordinates or a vector coordinate + multiplier and leftover
# First 2 coordinates will always result in a lesser magnitude vector
# For math computation and parallel non-vector generation of correct answer
# 3rd element should not be 0
params_coord_math_auto_verify_lt = [
    (1, 1, 1, 1.5),
    (0.9, 0, 1, 0),
    (1, -0, 2, -0),
    (-1, 0, 1, 0.5),
    (9/11, 2, 1.3, -2.5),
    (3/2, 1/3, 1.5, -2),
    (1, 0.01, 1, 0.1),
    (0, 1, 2, 3),
    (3, 2, 1, 9),
    (0, 2, 3, 1),
    (2, 3, 5, 1),
    (-2, -3, -5, -1),
    (math.sqrt(2), 1, math.sqrt(2), math.sqrt(2)),
    (0, EPSILON * 10, 1, 2),
    (EPSILON, 0, EPSILON, EPSILON * 10),
]

# Includes params_coord_math_auto_verify_lt and adds equal sized vectors
params_coord_math_auto_verify_le = params_coord_math_auto_verify_lt + [
    (3, 2, 3, 2),
    (3, -2, 3, 2),
    (-3, 2, 3, 2),
    (-3, -2, 3, 2),
    (math.sqrt(2), math.sqrt(2), math.sqrt(2), math.sqrt(2)),
    (math.sqrt(2), -math.sqrt(2), math.sqrt(2), math.sqrt(2)),
    (0.5, 1/3, 1/2, 0.33333333333333333),
    (0, EPSILON / 10, 2, 3),
    (0, EPSILON / 10, EPSILON, 3),
]

# Coordinates which include min and max float values
# Unreliable for use with mathematical tests
params_coord_math_auto_verify_inf = [
    (sys.float_info.max, sys.float_info.min, sys.float_info.max, sys.float_info.min),
    (sys.float_info.max, sys.float_info.min, 2, 2),
    (sys.float_info.max, 2, sys.float_info.max, 3),
]

# Invalid types for arithmetic, including multiplicitive operations
params_math_invalid_types_n_mul = [
    ('w',),
    (True,),
    (object(),),
    ('1',),
    ('2.5',),
]

# Invalid types for arithmetic, excluding multiplicitive operations
params_math_invalid_types_w_mul = params_math_invalid_types_n_mul + [
    (1,),
    (1.0,),
]

# Cartesian/Polar coordinate pairs
params_coords_x_y_m_polar_degree_radian = [
    (1, 0, 1, 0, 0),
    (0, 1, 1, 90, math.pi/2),
    (-1, 0, 1, 180, math.pi),
    (0, -1, 1, -90, 3*math.pi/2),
    (1, 1, math.sqrt(2), 45, math.pi/4),
    (-1, -1, math.sqrt(2), -135, 5*math.pi/4),
]


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le + params_coord_math_auto_verify_inf)
def test_vector_correct_value(x1, y1, x2, y2):
    p1 = Vector(x1, y1)
    assert p1.x == x1
    assert p1.y == y1
    p2 = Vector(x2, y2)
    assert p2.x == x2
    assert p2.y == y2


@pytest.mark.parametrize('tx,ty,ex,ey,et', [
    (1, 2, 1.0, 2.0, float),
    (sys.float_info.min, sys.float_info.min, float(sys.float_info.min), float(sys.float_info.min), float),
])
def test_vector_valid_conv(tx, ty, ex, ey, et):
    p1 = Vector(tx, ty)
    assert p1.x == ex
    assert p1.y == ey
    assert type(p1.x) is type(p1.y) is et


@pytest.mark.parametrize('x,y', [
    ('w', 0.0), (0.0, 'w'),
    (True, 0.0,), (0.0, True),
    ('1.0s', 0.0), (0.0, '1.0s'),
    ('1.0', 0.0), (0.0, '1.0'),
    (1, '0',), (0.0, '0'),
])
def test_vector_invalid_conv(x, y):
    with pytest.raises(TypeError, match=r'\'\w+\' must be a number$'):
        Point(x, y)


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_str(x1, y1, x2, y2):
    assert str(Vector(x1, y1)) == f'[{float(x1)}, {float(y1)}]'
    assert str(Vector(x2, y2)) == f'[{float(x2)}, {float(y2)}]'


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_eq(x1, y1, x2, y2):
    assert Vector(x1, y1) == Vector(x1, y1)
    assert Vector(x2, y2) == Vector(x2, y2)


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_lt + [
    (3, -2, 3, 2),
    (-3, 2, 3, 2),
    (-3, -2, 3, 2),
])
def test_vector_ne(x1, y1, x2, y2):
    v1 = Vector(x1, y1)
    v2 = Vector(x2, y2)
    assert v1 != v2


@pytest.mark.parametrize('x,y,s', [
    (3, -2, 5),
    (1, 1, math.sqrt(2)),
    (1, 1, '1.41'),
    (0, 1.5, 1.5),
])
def test_vector_ne_bad_types(x, y, s):
    v = Vector(x, y)
    assert v != s


@pytest.mark.parametrize('x,y,ox,oy', params_coord_math_auto_verify_le)
def test_vector_copy(x, y, ox, oy):
    v1 = Vector(x, y)
    v2 = copy.copy(v1)
    assert v1 == v2
    v1.x = v1.x + ox
    v1.y = v1.y + oy
    assert v1 != v2


@pytest.mark.parametrize('x,y,ox,oy', params_coord_math_auto_verify_le)
def test_vector_deepcopy(x, y, ox, oy):
    v1 = Vector(x, y)
    v2 = copy.copy(v1)
    assert v1 == v2
    v1.x = v1.x + ox
    v1.y = v1.y + oy
    assert v1 != v2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_vector_add(x1, y1, x2, y2):
    v1 = Vector(x1, y1)
    v2 = Vector(x2, y2)
    assert (v1 + v2).x == x1 + x2
    assert (v1 + v2).y == y1 + y2
    assert (v1 + v2 + v2).x == x1 + x2 + x2
    assert (v1 + v2 + v2).y == y1 + y2 + y2


@pytest.mark.parametrize('o2', params_math_invalid_types_w_mul)
def test_vector_vector_add_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'unsupported operand type(s) for +: \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 + o2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_vector_sub(x1, y1, x2, y2):
    v1 = Vector(x1, y1)
    v2 = Vector(x2, y2)
    assert (v1 - v2).x == v1.x - v2.x
    assert (v1 - v2).y == v1.y - v2.y
    assert (v1 - v2 - v2).x == v1.x - v2.x - v2.x
    assert (v1 - v2 - v2).y == v1.y - v2.y - v2.y


@pytest.mark.parametrize('o2', params_math_invalid_types_w_mul)
def test_vector_vector_sub_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'unsupported operand type(s) for -: \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 - o2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_vector_mul(x1, y1, x2, y2):
    v1 = Vector(x1, y1)
    v2 = Vector(x2, y2)
    d = x1 * x2 + y1 * y2
    assert v1 * v2 == d


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_vector_dot(x1, y1, x2, y2):
    v1 = Vector(x1, y1)
    v2 = Vector(x2, y2)
    d = x1 * x2 + y1 * y2
    assert v1.dot(v2) == d == v2.dot(v1)


@pytest.mark.parametrize('x,y,m,_', params_coord_math_auto_verify_le)
def test_vector_scalar_mul(x, y, m, _):
    v = Vector(x, y)
    assert (v * m).x == x * m
    assert (v * m).y == y * m
    assert (v * m * m).x == x * m * m
    assert (v * m * m).y == y * m * m


@pytest.mark.parametrize('o2', params_math_invalid_types_n_mul)
def test_vector_vector_mul_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'unsupported operand type(s) for *: \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 - o2


@pytest.mark.parametrize('x,y,m,_', params_coord_math_auto_verify_le)
def test_vector_scalar_truediv(x, y, m, _):
    v = Vector(x, y)
    assert (v / m).x == x / m
    assert (v / m).y == y / m
    assert (v / m / m).x == x / m / m
    assert (v / m / m).y == y / m / m


@pytest.mark.parametrize('o2', params_math_invalid_types_n_mul)
def test_vector_vector_truediv_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'unsupported operand type(s) for /: \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 / o2


@pytest.mark.parametrize('x,y,m,_', params_coord_math_auto_verify_le)
def test_vector_scalar_floordiv(x, y, m, _):
    v = Vector(x, y)
    assert (v // m).x == x // m
    assert (v // m).y == y // m
    assert (v // m // m).x == x // m // m
    assert (v // m // m).y == y // m // m


@pytest.mark.parametrize('o2', params_math_invalid_types_n_mul)
def test_vector_vector_floordiv_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'unsupported operand type(s) for //: \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 // o2


@pytest.mark.parametrize('x,y,_,__', params_coord_math_auto_verify_le)
def test_vector_neg(x, y, _, __):
    v = -Vector(x, y)
    assert v.x == -x
    assert v.y == -y


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_lt)
def test_vector_lt(x1, y1, x2, y2):
    assert Vector(x1, y1) < Vector(x2, y2)


@pytest.mark.parametrize('o2', params_math_invalid_types_n_mul)
def test_vector_lt_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'\'<\' not supported between instances of \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 < o2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_le(x1, y1, x2, y2):
    assert Vector(x1, y1) <= Vector(x2, y2)


@pytest.mark.parametrize('o2', params_math_invalid_types_n_mul)
def test_vector_le_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'\'<=\' not supported between instances of \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 <= o2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_lt)
def test_vector_gt(x1, y1, x2, y2):
    assert Vector(x2, y2) > Vector(x1, y1)


@pytest.mark.parametrize('o2', params_math_invalid_types_n_mul)
def test_vector_gt_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'\'>\' not supported between instances of \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 > o2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_ge(x1, y1, x2, y2):
    assert Vector(x2, y2) >= Vector(x1, y1)


@pytest.mark.parametrize('o2', params_math_invalid_types_n_mul)
def test_vector_ge_invalid(o2):
    v1 = Vector(1, 2)
    with pytest.raises(TypeError, match=re.escape(f'\'>=\' not supported between instances of \'{type(v1).__name__}\' and \'{type(o2).__name__}\'')):  # noqa: E501
        v1 = v1 >= o2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_vector_iadd(x1, y1, x2, y2):
    v1 = Vector(x1, y1)
    v1_copy = copy.copy(v1)
    v2 = Vector(x2, y2)
    v1 += v2
    assert v1.x == x1 + x2
    assert v1.y == y1 + y2
    assert v1 == v1_copy + v2

    v1 += v2
    assert v1.x == x1 + x2 + x2
    assert v1.y == y1 + y2 + y2
    assert v1 == v1_copy + v2 + v2


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_vector_isub(x1, y1, x2, y2):
    v1 = Vector(x1, y1)
    v1_copy = copy.copy(v1)
    v2 = Vector(x2, y2)
    v1 -= v2
    assert v1.x == x1 - x2
    assert v1.y == y1 - y2
    assert v1 == v1_copy - v2

    v1 -= v2
    assert v1.x == x1 - x2 - x2
    assert v1.y == y1 - y2 - y2
    assert v1 == v1_copy - v2 - v2


@pytest.mark.parametrize('x,y,m,_', params_coord_math_auto_verify_le)
def test_vector_vector_imul(x, y, m, _):
    v1 = Vector(x, y)
    v1_copy = copy.copy(v1)
    v1 *= m
    assert v1.x == x * m
    assert v1.y == y * m
    assert v1 == v1_copy * m

    v1 *= m
    assert v1.x == x * m * m
    assert v1.y == y * m * m
    assert v1 == v1_copy * m * m


@pytest.mark.parametrize('x,y,m,_', params_coord_math_auto_verify_le)
def test_vector_vector_itruediv(x, y, m, _):
    v1 = Vector(x, y)
    v1_copy = copy.copy(v1)
    v1 /= m
    assert v1.x == x / m
    assert v1.y == y / m
    assert v1 == v1_copy / m

    v1 /= m
    assert v1.x == x / m / m
    assert v1.y == y / m / m
    assert v1 == v1_copy / m / m


@pytest.mark.parametrize('x,y,m,_', params_coord_math_auto_verify_le)
def test_vector_vector_ifloordiv(x, y, m, _):
    v1 = Vector(x, y)
    v1_copy = copy.copy(v1)
    v1 //= m
    assert v1.x == x // m
    assert v1.y == y // m
    assert v1 == v1_copy // m

    v1 //= m
    assert v1.x == x // m // m
    assert v1.y == y // m // m
    assert v1 == v1_copy // m // m


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_magnitude(x1, y1, x2, y2):
    assert abs(Vector(x1, y1).magnitude - math.sqrt(x1*x1 + y1*y1)) < EPSILON
    assert abs(Vector(x2, y2).magnitude - math.sqrt(x2*x2 + y2*y2)) < EPSILON


@pytest.mark.parametrize('x,y,d', [
    (1, 0, 0), (1, 1, 45), (0, 1, 90),
    (-1, 0, 180), (-1, -1, -135), (math.sqrt(2), math.sqrt(2), 45),
])
def test_vector_angle(x, y, d):
    assert Vector(x, y).angle == d


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_normalize(x1, y1, x2, y2):
    for x_y in ((x1, y1), (x2, y2)):
        x, y = x_y[0], x_y[1]
        m = math.dist((0, 0), (x, y))
        assert Vector(x, y).normalize() == Vector(x / m, y / m)


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_as_cartesian(x1, y1, x2, y2):
    assert Vector(x1, y1).as_cartesian() == (x1, y1)
    assert Vector(x2, y2).as_cartesian() == (x2, y2)


@pytest.mark.parametrize('x,y,m,d,_', params_coords_x_y_m_polar_degree_radian)
def test_vector_as_polar(x, y, m, d, _):
    assert Vector(x, y).as_polar() == (m, d)


@pytest.mark.parametrize('x,y,m,d,_', params_coords_x_y_m_polar_degree_radian)
def test_vector_from_polar_degrees(x, y, m, d, _):
    assert Vector.from_polar_degrees(m, d) == Vector(x, y)


@pytest.mark.parametrize('x,y,m,_,r', params_coords_x_y_m_polar_degree_radian)
def test_vector_from_polar_radians(x, y, m, _, r):
    assert Vector.from_polar_radians(m, r) == Vector(x, y)


@pytest.mark.parametrize('m1,d1,m2,d2,c', [
    (40, 0, 60, 45, 1697)
])
def test_vector_cross(m1, d1, m2, d2, c):
    v1 = Vector.from_polar_degrees(m1, d1)
    v2 = Vector.from_polar_degrees(m2, d2)
    assert c - 0.5 < v1.cross(v2) < c + 0.5  # cross might have inaccuracy so give margin
    assert -c - 0.5 < v2.cross(v1) < -c + 0.5
    assert v1.cross(v2) == -(v2.cross(v1))


@pytest.mark.parametrize('x1,y1,x2,y2', params_coord_math_auto_verify_le)
def test_vector_from_origin(x1, y1, x2, y2):
    assert Vector.from_origin(Point(x1, y1)) == Vector(x1, y1)
    assert Vector.from_origin(Point(x2, y2)) == Vector(x2, y2)


def test_vector_unit_horizontal():
    assert Vector.unit_horizontal() == Vector(1, 0)


def test_vector_unit_vertical():
    assert Vector.unit_vertical() == Vector(0, 1)


def test_vector_unit_diagonal():
    assert Vector.unit_diagonal() == Vector(1/math.sqrt(2), 1/math.sqrt(2))


@pytest.mark.parametrize('v1,v2,w1,w2', [
    (1, 1, 0, 1),
    (0, 1, 0, -1),
    (-1, 0, 1, 0),
    (1, 1, 1, 1),
])
def test_vector_degrees_between(v1, v2, w1, w2):
    assert Vector(v1, v2).angle_between(Vector(w1, w2)) - math.degrees(math.atan2(w2*v1 - w1*v2, w1*v1 + w2*v2)) < EPSILON  # noqa: E501


def test_vector_from_positions():
    assert False
