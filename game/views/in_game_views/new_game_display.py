import pygame as pg

from game.views.in_game_views.game_menues_display import Game_menues_display
from game.views._option_menu_class_ import Option_menu_class

class In_battle_display(Game_menues_display):
    def init_in_battle_display(self):
        self.init_in_game_display()
        self.init_root_variables_new_game()

    def init_root_variables_new_game(self):
        self.init_root_variables_in_game()
        
        self.player_input_variables : tuple = (
            self.width*0.5, self.height*0.5, 60
        )
        self.pokemon_choice_variables : tuple = (
            self.width*0.5, self.height*0.7, 60
        )

    def init_menues_objects(self):
        self.player_input = Input_menu_class(
            self.player_input_variables,
        )
        self.pokemon_choice = Option_menu_class(
            self.pokemon_choice_variables,
            [
                self.dialogs["bulbasaur"],
                self.dialogs["charmander"],
                self.dialogs["squirtle"]
            ]
        )