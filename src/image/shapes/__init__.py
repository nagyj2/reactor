from .circle import Circle  # noqa: F401
from .constants import shape_batch as _shape_batch
from .rectangle import Rectangle  # noqa: F401
from .shapes import Layer  # noqa: F401


def draw_primitives():
    _shape_batch.draw()
