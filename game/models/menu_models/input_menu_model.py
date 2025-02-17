import pygame as pg
import string

from game.views.display import Display

class Input_menu_model(Display):
    def __init__(self, margins : tuple, dialog : str):
        Display.__init__(self)
        self.from_left, self.from_top = margins
        self.dialog = dialog
        self.input = ""
        self.input_color = (0,0,0)
        self.pre_render()
    
    def pre_render(self):
        self.rendered_input = self.pixel_font_menu_deselected.render(self.dialog + self.input, True, self.input_color)
        self.rendered_input_rect = self.rendered_input.get_rect(center=(self.from_left, self.from_top))
    
    def draw_input(self):
        self.pre_render()
        self.screen.blit(self.rendered_input, self.rendered_input_rect)

    def get_event_input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE and self.input != "":
                self.input = self.input[:-1]

            elif len(self.input) <= 9:
                if str(event.unicode).upper() in string.ascii_uppercase or event.unicode in (" ", "-", "'"):
                    self.input += event.unicode