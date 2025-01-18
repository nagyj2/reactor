
import pyglet

from GraphicalEntity import PointEntity
from Shapes import Layer

# todo:
# add fast variant (rquires moderation to slow)

WHITE = (255, 255, 255, 255)
LIFETIME = 10


class Neutron(PointEntity):
    def __init__(self, x, y, dx, dy, radius):
        super().__init__(x, y, dx, dy, WHITE, radius)

        self.image.set_layer(Layer.FOREGROUND)
        pyglet.clock.schedule_once(self.kill, LIFETIME)

    # @static_update_function
    # def _draw(self):
    #     self.image.radius = self.radius
    #     super().draw()

    # @static_update_function
    # def _update(self, dt):
    #     super().update(dt)

    # def _move(self, dt):
    #     super().move(dt)

    # @static_update_function
    # def _prepare(self):
    #     super().prepare()
