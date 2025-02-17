import pygame as pg

from game.control.control import Control
from game._all_paths_ import MUSIC_PATH, SFX_PATH, GRAPHICS_PATH

class Sounds(Control):
    def __init__(self):
        self.init_config()
        self.MUSIC_PATH = MUSIC_PATH
        self.SFX_PATH = SFX_PATH
        self.GRAPHICS_PATH = GRAPHICS_PATH
