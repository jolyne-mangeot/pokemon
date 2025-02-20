import pygame as pg

from game.control.control import Control
from game._all_paths_ import MUSIC_PATH, SFX_PATH, GRAPHICS_PATH

class Sounds(Control):
    """
        The Sounds class inherits from Control and is responsible for managing sound effects and music.
        It initializes paths to the sound assets and provides methods to load and manage sounds.
    """
    def __init__(self):
        self.init_config()
        self.MUSIC_PATH = MUSIC_PATH
        self.SFX_PATH = SFX_PATH
        self.GRAPHICS_PATH = GRAPHICS_PATH
    
    def init_sounds(self):
        self.music_channel = pg.mixer.Channel(0)
        self.music_channel.set_volume(self.music_volume*0.1)
        self.effects_channel = pg.mixer.Channel(1)
        self.effects_channel.set_volume(self.sfx_volume*0.4)
