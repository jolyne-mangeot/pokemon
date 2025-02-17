import pygame as pg

from game.views.in_game_views.game_menues_display import Game_menues_display
from game.views._option_menu_class_ import Option_menu_class

class Launch_menu_display(Game_menues_display):
    def init_launch_menu_display(self):
        self.init_in_game_display()
        self.init_root_variables_launch_menu()
        self.init_menues_objects()

    def init_root_variables_launch_menu(self):
        width : int = self.screen_rect.width
        height : int = self.screen_rect.height

        self.confirm_menu_variables : tuple = (
            width/2, height/2, 60
        )
        self.main_menu_variables : tuple = (
            width/2, height/2, 60
        )
    
    def init_menues_objects(self):
        self.main_launch_menu = Option_menu_class(
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
        self.manage_team_menu = Option_menu_class(
            self.main_menu_variables,
            self.init_render_option_team(self.player_pokedex.player_team)
        )
        self.confirm_action_menu = Option_menu_class(
            self.confirm_menu_variables,
            [self.dialogs["no"], self.dialogs["yes"]],
        )
        self.save_menu = Option_menu_class(
            self.main_menu_variables,
            [
                self.dialogs["save_1"],
                self.dialogs["save_2"],
                self.dialogs["back"]
            ]
        )