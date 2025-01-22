
import configparser
import os

config_filename = 'config'


class Settings(object):
    PHYSICS_DIVISIONS = 8

    def __new__(cls):  # make a singleton class
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def load_settings(self, config, default=False):
        self.WIDTH = config.getint('screen', 'width') if not default else 640
        self.HEIGHT = config.getint('screen', 'height') if not default else 480
        self.FPS = config.getint('screen', 'fps') if not default else 30

        self.PHYSICS_GRID = config.getboolean('physics', 'grid') if not default else False

        self.TITLE = "RBMK Reactor Simulation"
        self.entity_id = 0  # provided to all Entities and incremented

    def next_id(self):
        self.entity_id += 1
        return self.entity_id - 1


GlobalSettings = Settings()


def init_settings(default=True):
    global GlobalSettings, config_filepath

    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, config_filename)

    config = configparser.ConfigParser()
    config.read(initfile)
    GlobalSettings.load_settings(config)
