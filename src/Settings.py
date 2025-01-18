
import configparser
import os

config_filename = 'config'


class Settings(object):
    def __new__(cls):  # make a singleton class
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    def load_settings(self, config):
        self.WIDTH = int(config.get('screen', 'width'))
        self.HEIGHT = int(config.get('screen', 'height'))
        self.FPS = float(config.get('screen', 'fps'))
        self.TITLE = "RBMK Reactor Simulation"


GlobalSettings = Settings()


def init_settings():
    global GlobalSettings, config_filepath

    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, config_filename)

    config = configparser.RawConfigParser()
    config.read(initfile)
    GlobalSettings.load_settings(config)
