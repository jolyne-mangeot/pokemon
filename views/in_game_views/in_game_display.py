import pygame as pg

from views.display import Display
from assets.__graphics_settings__ import GRAPHICS_PATH

class In_game_display(Display):
    def init_in_game_display(self):
        self.init_root_variables_in_game()
        self.load_graphics_pokemons()

    def init_root_variables_in_game(self):
        width : int = self.screen_rect.width
        height : int = self.screen_rect.height

        self.active_pokemon_image_size : tuple = (width*0.3, width*0.3)
        self.mini_image_size : tuple = (width*0.21, width*0.2)

    def load_graphics_pokemons(self):
        for pokemon in self.player_pokedex.player_team:
            back_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/back.png")
            pokemon.back_image = pg.transform.scale(back_image, self.active_pokemon_image_size)
            mini_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/mini.png")
            pokemon.mini_image = pg.transform.scale(mini_image, self.mini_image_size)

    def pre_render_options(self):
        """
            Selects a font and pre-renders it regardless of hovered / selected
            option. all for display
        """
        rendered_dialog = {"deselected":[], "selected":[]}
        if self.rendered_picked != {}:
            rendered_dialog.update(self.rendered_picked)
        for option in self.options:
            deselected_render = self.pixel_font_menu_deselected.render(option, 1, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            selected_render = self.pixel_font_menu_selected.render(option, 1, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_dialog["deselected"].append((deselected_render, deselected_rect))
            rendered_dialog["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_dialog
        return rendered_dialog
    
    def init_render_option_confirm(self):
        self.from_left, self.from_top, self.spacer = self.confirm_menu_variables
        self.options = [
            self.dialogs["no"],
            self.dialogs["yes"]
            ]
    
    def init_render_option_team(self, team, forced_switch=False, team_full=False):
        options = []
        for pokemon in team:
            options.append(self.dialogs[pokemon.name])
        while len(options) < 6:
            options.append("")
        if not forced_switch and not team_full:
            options.append(self.dialogs['back'])
        return options
        

    def pre_render_team(self):
        rendered_dialog = {"picked" : [], "deselected":[], "selected":[]}

        for option in self.options:
            picked_render = self.pixel_font_menu_selected.render(option, True, self.picked_color)
            picked_rect = picked_render.get_rect()
            deselected_render = self.pixel_font_menu_deselected.render(option, True, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            selected_render = self.pixel_font_menu_selected.render(option, True, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_dialog["picked"].append((picked_render, picked_rect))
            rendered_dialog["deselected"].append((deselected_render, deselected_rect))
            rendered_dialog["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_dialog
        self.rendered_team = rendered_dialog
