
from pyglet.window import key

from Controller import Controller, KeyEvent, KeyMap
from GraphicalEntity import RectangleEntity
from Shapes import Layer

# Todo:
# Better way to handle vel reset w/ controller

DARK_GRAY = (99, 99, 99, 255)


def controlrod_controls(arrows, speed, minx, maxx, miny, maxy):
    def go_up(entity, dt):
        if entity.top_left.y < maxy:
            entity.vel.y += speed
    hold_up = KeyMap(key.UP if arrows else key.W, None, KeyEvent.HELD, go_up)

    def go_down(entity, dt):
        if entity.bottom_left.y > miny:
            entity.vel.y -= speed
    hold_down = KeyMap(key.DOWN if arrows else key.S, None, KeyEvent.HELD, go_down)

    return (hold_up, hold_down)


class ControlRod(RectangleEntity):
    def __init__(self, x, y, w, h, speed, minx, maxx, miny, maxy, window):
        super().__init__(x, y, 0, 0, DARK_GRAY, w, h)
        self.controller = Controller(self, window, controlrod_controls(True, speed, minx, maxx, miny, maxy))
        self.repr.append(self.controller)

        self.image.set_layer(Layer.MIDGROUND)
