import pygame as pg

from game.control.control import Control
from game._all_paths_ import GRAPHICS_PATH, FONTS_PATH, POKEMON_CLASSIC_FONT

class Display(Control):
    def __init__(self):
        self.init_config()
        self.width : int = self.screen_rect.width
        self.height : int = self.screen_rect.height

        self.GRAPHICS_PATH = GRAPHICS_PATH
        self.FONTS_PATH = FONTS_PATH
        self.POKEMON_CLASSIC_FONT = POKEMON_CLASSIC_FONT

        self.pixel_font_pokemon_infos = pg.font.Font(self.FONTS_PATH + self.POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.022))
        self.pixel_font_menu_deselected = pg.font.Font(self.FONTS_PATH + self.POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.022))
        self.pixel_font_menu_selected = pg.font.Font(self.FONTS_PATH + self.POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.025))