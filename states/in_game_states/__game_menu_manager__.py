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
        self.rendered_picked = {}
        self.last_option = None
        self.picked_index = None
        self.selected_color = (255,255,0)
        self.deselected_color = (255,255,255)
        self.picked_color = (255,0,0)
    
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
        if self.rendered_picked != {}:
            rendered_dialog.update(self.rendered_picked)
        for option in self.options:
            deselected_render = font_deselected.render(option, 1, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            selected_render = font_selected.render(option, 1, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_dialog["deselected"].append((deselected_render, deselected_rect))
            rendered_dialog["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_dialog
    
    def pre_render_team(self):
        font_picked = pg.font.SysFont("arial", 40)
        rendered_dialog = {"picked" : []}
        for option in self.options:
            picked_render = font_picked.render(option, 1, self.picked_color)
            picked_rect = picked_render.get_rect()
            rendered_dialog["picked"].append((picked_render, picked_rect))
        self.rendered_picked = rendered_dialog
    
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
        self.from_top = self.screen_rect.height/2
        self.spacer = 60
        self.options = [
            self.dialogs["no"],
            self.dialogs["yes"]
            ]
    
    def init_render_option_team(self):
        self.from_top = self.screen_rect.height*0.1
        self.spacer = 50
        self.options = []
        for pokemon in self.player_pokedex.player_team:
            self.options.append(self.dialogs[pokemon.name])
        while len(self.options) < 6:
            self.options.append("")
        self.options.append(self.dialogs['back'])

    def get_event_quit(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit or\
                pg.key.name(event.key) in self.confirm_keys and self.selected_index == 0:
                self.menu_state = self.back
                self.update_options()
            elif pg.key.name(event.key) in self.confirm_keys and self.selected_index == 1:
                self.next = "main_menu"
                self.done = True
                self.selected_index = 0
    
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