
import configparser
import os

config_filename = 'config'


class Settings(object):
    def __new__(cls):  # make a singleton class
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def load_settings(self, config):
        self.WIDTH = config.getint('screen', 'width')
        self.HEIGHT = config.getint('screen', 'height')
        self.FPS = config.getint('screen', 'fps')

        self.TITLE = "RBMK Reactor Simulation"
        self.entity_id = 0  # provided to all Entities and incremented


GlobalSettings = Settings()


def init_settings():
    global GlobalSettings, config_filepath

    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, config_filename)

    config = configparser.ConfigParser()
    config.read(initfile)
    GlobalSettings.load_settings(config)
