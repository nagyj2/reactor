
# from copy import deepcopy

import pyglet

from Atom import Atom
from ControlRod import ControlRod
from Emitter import get_per_frame_chance
from Moveable import Moveable
from Neutron import Neutron
from Settings import init_settings
from Shapes import draw_primitives
from Water import Water

# may be needed on MacOS to prevent screen from having issues due to high DPI
pyglet.options.dpi_scaling = 'stretch'

TITLE = 'Reactor Simulation'
WIDTH, HEIGHT = 640, 480
FPS = 60


if __name__ == '__main__':
    init_settings()
    window = pyglet.window.Window(width=WIDTH, height=HEIGHT, caption=TITLE)

    SPEED = 50

    entities = []
    to_add = []

    n = Neutron(100, 100, SPEED, -SPEED*2, 3)
    w = Water(WIDTH/2, 0, WIDTH/2, HEIGHT/2)
    a = Atom(WIDTH/2, HEIGHT/2, 0, 0, 10, 3, get_per_frame_chance(0.5, FPS), Neutron(0, 0, SPEED, -SPEED*2, 3), to_add)  # noqa: E501
    c = ControlRod(150, 50, 10, HEIGHT-150, 10, 0, WIDTH, 0, HEIGHT, window)
    m = Moveable(100, 200, SPEED, 5, window, tuple())

    entities += [c, w, n, m, a]

    for i in entities:
        print(i)

    tt = 0.0  # track time for printing

    def update(dt):
        global tt, entities, to_add

        ott = tt
        tt = (tt + dt) % 5
        if tt < ott:
            print(f'Simulation Size: {len(entities)}')

        # GENERAL LOGIC
        for e in entities:
            e.update(dt)

        # Bounce 'super' neutron on walls and c
        if n.pos.x > WIDTH:
            n.pos.x = WIDTH - n.vel.x * dt  # snap x and y to in bounds
            n.vel.x *= -1
        elif n.pos.x < 0:
            n.pos.x = -n.vel.x * dt
            n.vel.x *= -1
        if n.pos.y > HEIGHT:
            n.pos.y = HEIGHT - n.vel.y * dt
            n.vel.y *= -1
        elif n.pos.y < 0:
            n.pos.y = -n.vel.y * dt
            n.vel.y *= -1
        for o in (c, w):
            if n in o:
                n.pos -= n.vel * dt
                if o.left_x < n.pos.x < o.right_x:  # if top/bottom or left/right reflection
                    n.vel.y *= -1
                else:
                    n.vel.x *= -1

        # Check for entity events
        iw = 1  # entities in water (itself)
        for e in entities:
            # Delete neutrons that have gone too far
            if type(e) is Neutron and e is not n:
                KILL_RANGE = 50
                MAX_X = WIDTH - KILL_RANGE
                MIN_X = 0 + KILL_RANGE
                MAX_Y = HEIGHT - KILL_RANGE
                MIN_Y = 0 + KILL_RANGE
                if e.pos.x > MAX_X \
                        or e.pos.x < MIN_X \
                        or e.pos.y > MAX_Y \
                        or e.pos.y < MIN_Y:

                    e.image.color = (255, 0, 0)
                    e.alive = False

            # Update water's colour dpending on how much stuff is in it
            if e in w:
                iw += 1
        w.image.color = (*map(lambda c: c - c * (iw//len(entities)), (0, 0, 255)), 255)

        # UPDATE POSITIONS
        for e in entities:
            e.move(dt)

        # UPDATE VISUAL ELEMENTS
        for e in entities:
            e.draw()

        # PREPARE ELEMENTS
        for e in entities:
            e.prepare()

        # DELETE ELEMENTS
        entities = list(filter(lambda e: e.alive is True, entities))
        # for e in list(filter(lambda e: e.alive is False, entities)):  # fix: kills objects it shouldnt
        #     entities.remove(e)
        entities.extend(to_add)
        to_add.clear()  # fed into other objects so must maintain reference

    pyglet.clock.schedule_interval(update, 1/FPS)

    @window.event
    def on_draw():
        window.clear()
        draw_primitives()

    pyglet.app.run()
