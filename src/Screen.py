
import pyglet

from Atom import Atom
from ComplexImage import ScreenGrid
from ControlRod import ControlRod
from Emitter import TestEmitter, get_per_frame_chance
from Moveable import Moveable
from Neutron import Neutron
from Physics import GlobalPhysics as Physics
from Settings import GlobalSettings as Settings
from Shapes import draw_primitives
from SimpleGraphicalEntity import PointEntity
from Thermal import Thermal
from Water import Water

# todo:
# add static to graphical entities

pyglet.options.dpi_scaling = 'stretch'


class Game:
    def __init__(self):
        self.restart_game()

    def restart_game(self):
        self._initialize_states()
        self._initialize_screen()
        self._initialize_game()

    def _initialize_states(self):
        KILL_BORDER = 50
        self.MAX_X = Settings.WIDTH - KILL_BORDER
        self.MIN_X = 0 + KILL_BORDER
        self.MAX_Y = Settings.HEIGHT - KILL_BORDER
        self.MIN_Y = 0 + KILL_BORDER

        self.DEFAULT_SPEED = 50

        Thermal.register_transfer_coefficient(Water, Moveable, 1)
        Thermal.register_dissipation_coefficient(Water, 0.15)
        Thermal.register_dissipation_coefficient(Moveable, 1)

        # State variables
        self.tt = 0.0  # track time for printing
        self.iter = 0  # iterations between prints

    def _initialize_screen(self):
        window = pyglet.window.Window(width=Settings.WIDTH,
                                      height=Settings.HEIGHT,
                                      caption=Settings.TITLE)

        @window.event
        def on_draw():
            window.clear()
            draw_primitives()

        self.window = window

    def _initialize_game(self):
        # place atoms
        # place water
        # place control rods

        self.gui = []
        self.new_entities = []
        self.cur_entities = [
            TestEmitter(Settings.WIDTH/2, Settings.HEIGHT/2, 3, 1, 3, self.new_entities),
            Water(Settings.WIDTH/2, 0, Settings.WIDTH/2, Settings.HEIGHT/2),
            # Atom(Settings.WIDTH/2, Settings.HEIGHT/2, 0, 0, 10, 3, get_per_frame_chance(10, Settings.FPS), Neutron(0, 0, self.DEFAULT_SPEED, 0, 3), self.new_entities),  # noqa: E501)
            # ControlRod(150, 50, 10, Settings.HEIGHT-150, 10, 0, Settings.WIDTH, 0, Settings.HEIGHT, self.window),
            Moveable(100, 100, self.DEFAULT_SPEED, 5, self.window, tuple())
        ]

        for e in self.cur_entities:
            Physics.add_to_sector(e)

        if Settings.PHYSICS_GRID:
            self.gui.append(ScreenGrid(0, 0, Settings.PHYSICS_DIVISIONS, Settings.PHYSICS_DIVISIONS, 3, (32, 32, 32)))

    def _game_loop(self, dt):
        ott = self.tt
        self.tt = (self.tt + dt) % 5
        self.iter += 1
        if self.tt < ott:
            print(f'Simulation Size:  {len(self.cur_entities)}, iter={self.iter}')
            print(f'Physics Entities: {len(Physics.get_registered_entities())}')
            self.iter = 0

        # GENERAL LOGIC
        for e in self.cur_entities:
            e.update(dt)

        # PHYSICS
        for e1 in Physics.get_registered_entities():
            # Collisions
            for e2 in Physics.get_neighbour_entities(e1):
                if e1.id == e2.id:
                    continue
                if e1 in e2:
                    if type(e2) is Water and not e1.static and not e2.static:
                        e1.pos -= e1.vel * dt
                        if e2.left_x < e1.pos.x < e2.right_x:  # if top/bottom or left/right reflection
                            e1.vel.y *= -1
                        else:
                            e1.vel.x *= -1

                    if type(e1) is Water and type(e2) is Moveable:
                        e1.thermal.transfer(e2.thermal, dt)

            # Static Events
            if type(e1) is PointEntity \
                    and (e1.pos.x > self.MAX_X
                         or e1.pos.x < self.MIN_X
                         or e1.pos.y > self.MAX_Y
                         or e1.pos.y < self.MIN_Y):
                e1.alive = False

            if type(e1) is PointEntity and not e1.alive:
                e1.color = (255, 0, 0)

        Physics.update_sectors(Physics.get_registered_entities())

        # UPDATE POSITIONS
        for e in self.cur_entities:
            e.move(dt)

        # PREPARE ELEMENTS
        for e in self.cur_entities:
            e.prepare()

        # DELETE ELEMENTS
        self.cur_entities = list(filter(lambda e: e.alive is True, self.cur_entities))
        # for e in list(filter(lambda e: e.alive is False, entities)):  # fix: kills objects it shouldnt
        #     entities.remove(e)
        self.cur_entities.extend(self.new_entities)
        self.new_entities.clear()  # fed into other objects so must maintain reference

    def start_game(self):
        pyglet.clock.schedule_interval(self._game_loop, 1/Settings.FPS)
        pyglet.app.run()
