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
        self.POKEMON_CLASSIC_PATH = self.FONTS_PATH + self.POKEMON_CLASSIC_FONT

        self.pixel_font_pokemon_infos = pg.font.Font(self.POKEMON_CLASSIC_PATH, int(self.width*0.022))
        self.pixel_font_menu_deselected = pg.font.Font(self.POKEMON_CLASSIC_PATH, int(self.width*0.022))
        self.pixel_font_menu_selected = pg.font.Font(self.POKEMON_CLASSIC_PATH, int(self.width*0.025))
    
    def blit_dialog(self, dialog : str, size : int, from_left, from_top, placement_origin : str = "midbottom", color : tuple=(0,0,0), bold : bool=False):
        font = pg.font.Font(self.POKEMON_CLASSIC_PATH, int(size))
        font.set_bold(bold)
        text = font.render(dialog, True, color)
        if placement_origin == "midbottom":
            text_rect = text.get_rect(midbottom=(from_left,from_top))
        elif placement_origin == "bottomleft":
            text_rect = text.get_rect(bottomleft=(from_left,from_top))
        self.screen.blit(text, text_rect)

