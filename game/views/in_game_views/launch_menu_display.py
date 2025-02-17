import pygame as pg

from game.views.in_game_views.game_menues_display import Game_menues_display
from game.models.menu_models.option_menu_model import Option_menu_model

class Launch_menu_display(Game_menues_display):
    def init_launch_menu_display(self):
        self.init_in_game_display()
        self.init_root_variables_launch_menu()
        self.init_menues_objects()

    def init_root_variables_launch_menu(self):

        self.confirm_menu_variables : tuple = (
            self.width/2, self.height/2, 60
        )
        self.main_menu_variables : tuple = (
            self.width/2, self.height*0.36, self.height*0.09
        )
    
    def init_menues_objects(self):
        self.main_launch_menu = Option_menu_model(
            self.main_menu_variables,
            [
                self.dialogs["launch"],
                self.dialogs["manage met pokemons"],
                self.dialogs["manage team"],
                self.dialogs["save"],
                self.dialogs["quit"]
            ],
            ["launch_battle_confirm", "manage_settings", "manage_team", "save", "quit"]
        )
        self.manage_team_menu = Option_menu_model(
            self.main_menu_variables,
            self.init_render_option_team(self.player_pokedex.player_team)
        )
        self.confirm_action_menu = Option_menu_model(
            self.confirm_menu_variables,
            [self.dialogs["no"], self.dialogs["yes"]],
        )
        self.save_menu = Option_menu_model(
            self.main_menu_variables,
            [
                self.dialogs["save_1"],
                self.dialogs["save_2"],
                self.dialogs["back"]
            ]
        )
        self.main_launch_menu.update_colors((0,0,0),(80,96,176))