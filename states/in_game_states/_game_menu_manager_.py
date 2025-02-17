import pygame as pg
import string

from views.in_game_views.in_game_display import In_game_display

class Game_menu_manager(In_game_display):
    def __init__(self):
        """
            inits selected option, last option to check for on-same-button
            mouse-hover, and misc. values like font color. for all main_menu
            derived classes
        """
        pass
    
    def update_menu(self):
        """
            update_menu checks for all changes keyboard or mouse
            related
        """
        pass
    
    def get_event_player_input(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys:
                return False
            elif pg.key.name(event.key) in self.confirm_keys and self.player_input != "":
                return True

            elif event.key == pg.K_BACKSPACE and self.player_input != "":
                self.player_input = self.player_input[:-1]

            elif len(self.player_input) <= 9:
                if str(event.unicode).upper() in string.ascii_uppercase or event.unicode in (" ", "-", "'"):
                    self.player_input += event.unicode
        return None

    def draw_player_input(self, dialog : str):
        player_input_render = pg.font.SysFont("arial", 40).render(dialog + self.player_input, 1, self.deselected_color)
        player_input_rect = player_input_render.get_rect(center = self.screen_rect.center)
        self.screen.blit(player_input_render, player_input_rect)