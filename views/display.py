import pygame as pg
from assets.__graphics_settings__ import GRAPHICS_PATH
from assets.__fonts_settings__ import FONTS_PATH, POKEMON_CLASSIC_FONT

class Display:
    def __init__(self):
        self.pixel_font = pg.font.Font(FONTS_PATH + POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.02))

    def draw_menu_options(self):
        """
            for all launch_menu states, enumerate buttons and places them before
            checking for selected index button to place it on the same position
        """
        for index, option in enumerate(self.rendered["deselected"]):
            option[1].center = (self.from_left, self.from_top + index*self.spacer)
            if index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])
    
    def draw_confirm_options(self):
        for index, option in enumerate(self.rendered["deselected"]):
            if len(self.rendered["deselected"]) == 2:
                option[1].center = (self.screen_rect.centerx-50 + index*100, self.from_top)
            else:
                option[1].center = (self.screen_rect.centerx-200 + index*200, self.from_top)
            if index == self.selected_index:
                if bool(self.picked_index):
                    if self.selected_index == self.picked_index:
                        continue
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])
    
    def draw_picked(self):
        for index, option in enumerate(self.rendered["picked"]):
            option[1].center = (self.screen_rect.centerx, self.from_top + index*self.spacer)
            if index == self.picked_index:
                selected_render = self.rendered["picked"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])

    def load_graphics_main_menues(self):
        # self.background = pygame.
        # 
        # 
        pass

    def load_graphics_preferences_menu(self):
        # self.background = 
        pass

    def load_graphics_in_fight(self):
        pass