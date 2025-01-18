
import enum

from pyglet.window import key as pgkey

from Entity import Entity

# Todo:


class KeyEvent(enum.Enum):
    DOWN = 1  # event on keydown
    UP = 2  # event on keyup
    HELD = 3  # event on key being held


class KeyMap:
    def __init__(self, key, modifier, keyevent, action, order=0):
        self.key = key  # if hasattr(key, '__iter__') else (key,)
        self.modifier = modifier
        self.keyevent = keyevent
        self.action = action
        self.order = order  # lower is checked first


def wsad_controls(speed):
    # do not mult by dt b/c move() already handles that
    # use += and -= b/c pressing 2 directions at once will cancel movement, though requires manual reset of velocity
    def go_right(entity, dt):
        entity.vel.x += speed
    hold_right = KeyMap(pgkey.D, None, KeyEvent.HELD, go_right)

    def go_left(entity, dt):
        entity.vel.x -= speed
    hold_left = KeyMap(pgkey.A, None, KeyEvent.HELD, go_left)

    def go_up(entity, dt):
        entity.vel.y += speed
    hold_up = KeyMap(pgkey.W, None, KeyEvent.HELD, go_up)

    def go_down(entity, dt):
        entity.vel.y -= speed
    hold_down = KeyMap(pgkey.S, None, KeyEvent.HELD, go_down)

    def double_speed(entity, dt):
        entity.vel.x *= 2
        entity.vel.y *= 2
    press_shift = KeyMap(pgkey.LSHIFT, None, KeyEvent.HELD, double_speed, 1)

    return (hold_up, hold_down, hold_left, hold_right, press_shift)


class Controller(Entity):
    def __init__(self, parent, window, keymapping):
        super().__init__()
        self.parent = parent

        self.key_down = {}  # map of keys to check on key down and their action
        self.key_up = {}    # map of keys to check on key down and their action
        self.key_held = {}  # map of keyboard check layers containing keys and their action

        for keymap in keymapping:
            match keymap.keyevent:
                case KeyEvent.DOWN:
                    self.key_down[keymap.key] = keymap.action
                case KeyEvent.UP:
                    self.key_up[keymap.key] = keymap.action
                case KeyEvent.HELD:
                    if keymap.order not in self.key_held:
                        self.key_held[keymap.order] = {}
                    self.key_held[keymap.order][keymap.key] = keymap.action

        def on_key_press(symbol, modifier):
            # print(f'DOWN {symbol}')
            for key in self.key_down:
                if symbol == key:
                    self.key_down[key](self.parent, 0)

        def on_key_release(symbol, modifier):
            # print(f'UP {symbol}')
            for key in self.key_up:
                if symbol == key:
                    self.key_up[key](self.parent, 0)

        window.push_handlers(on_key_press)
        window.push_handlers(on_key_release)

        self.keys = pgkey.KeyStateHandler()  # Own key state
        window.push_handlers(self.keys)

    def _update(self, dt):
        super()._update(dt)

        for order in range(min(self.key_held.keys()), max(self.key_held.keys())+1):
            for key in self.key_held[order]:
                if self.keys[key]:
                    self.key_held[order][key](self.parent, dt)

    def _prepare(self):
        super()._prepare()

        self.parent.vel.x = 0  # controller handles movement so reset host's vel
        self.parent.vel.y = 0


class BasicController(Controller):
    def __init__(self, parent, speed, window, keymapping):
        super().__init__(parent, window,
                         keymapping + wsad_controls(speed))
