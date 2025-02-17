import pygame as pg

from control.control import Control
from assets._graphics_settings_ import GRAPHICS_PATH
from assets._fonts_settings_ import FONTS_PATH, POKEMON_CLASSIC_FONT

class Display(Control):
    def __init__(self):
        self.init_config()
        self.GRAPHICS_PATH = GRAPHICS_PATH
        self.FONTS_PATH = FONTS_PATH
        self.POKEMON_CLASSIC_FONT = POKEMON_CLASSIC_FONT

        self.pixel_font_pokemon_infos = pg.font.Font(self.FONTS_PATH + self.POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.02))
        self.pixel_font_menu_deselected = pg.font.Font(self.FONTS_PATH + self.POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.02))
        self.pixel_font_menu_selected = pg.font.Font(self.FONTS_PATH + self.POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.025))