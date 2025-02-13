import pygame as pg
import string

class Game_menu_manager:
    def __init__(self):
        """
            inits selected option, last option to check for on-same-button
            mouse-hover, and misc. values like font color. for all main_menu
            derived classes
        """
        self.selected_index = 0
        self.last_option = None
        self.selected_color = (255,255,0)
        self.deselected_color = (255,255,255)
    
    def update_menu(self):
        """
            update_menu checks for all changes keyboard or mouse
            related
        """
        pass
    
    def pre_render_options(self):
        """
            Selects a font and pre-renders it regardless of hovered / selected
            option. all for display
        """
        font_selected = pg.font.SysFont("arial", 40)
        font_deselected = pg.font.SysFont("arial", 40)

        rendered_dialog = {"deselected":[], "selected":[]}
        for option in self.options:
            deselected_render = font_deselected.render(option, 1, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            selected_render = font_selected.render(option, 1, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_dialog["deselected"].append((deselected_render, deselected_rect))
            rendered_dialog["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_dialog
    
    def change_selected_option(self, operant):
        """
            for keyboard behaviour, change based on operant the selected
            option : single direction for now (up or down)
        """
        self.selected_index += operant
        max_indicator = len(self.rendered["deselected"]) - 1
        if self.selected_index < 0:
            self.selected_index = max_indicator
        elif self.selected_index > max_indicator:
            self.selected_index = 0

    def init_render_option_confirm(self):
        self.from_top = self.screen_rect.height/2 - 60
        self.spacer = 60
        self.options = ["no", "yes"]

    def get_event_quit(self, event, back : str):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit or\
                pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = back
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                self.next = "main_menu"
                self.done = True
                self.selected_index = 0
    
    def get_event_player_input(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False, user_input

            if event.key == pg.K_RETURN and user_input != '':
                return True, user_input

            elif event.key == pg.K_BACKSPACE and user_input != '':
                user_input = user_input[:-1]
                return '', user_input

            elif len(user_input) <= 9:
                if str(event.unicode).upper() in string.ascii_uppercase or event.unicode in (" ", "-", "'"):
                    user_input += event.unicode
                    return '', user_input

    def draw_player_input(self, dialog : str):
        pass