import pygame as pg

from game.views.in_game_views.game_menues_display import Game_menues_display
from game.models.menu_models.option_menu_model import Option_menu_model
from game.models.menu_models.input_menu_model import Input_menu_model

class New_game_display(Game_menues_display):
    def init_new_game_display(self):
        self.display_init()
        self.init_root_variables_new_game()
        self.init_menues_objects()
        self.init_pokemon_starters_mini()
    
    def init_pokemon_starters_mini(self):
        self.pokemon_starters_image = []
        for pokemon in self.pokemon_starters:
            mini_image = pg.image.load(self.GRAPHICS_PATH + "pokemon/" + pokemon["entry"] + "/mini.png")
            mini_image = pg.transform.scale(mini_image, (self.width*0.5, self.width*0.42))
            self.pokemon_starters_image.append(mini_image)

    def init_root_variables_new_game(self):
        self.init_root_variables_in_game()
        
        self.player_input_variables : tuple = (
            self.width*0.5, self.height*0.5
        )
        self.pokemon_choice_variables : tuple = (
            self.width*0.5, self.height*0.6, 60
        )

    def init_menues_objects(self):
        self.player_input = Input_menu_model(
            self.player_input_variables,
            self.dialogs["your name"]
        )
        options = [self.dialogs[pokemon["name"]] for pokemon in self.pokemon_starters]
        self.pokemon_choice = Option_menu_model(
            self.pokemon_choice_variables,
            options
        )
        self.pokemon_choice.update_colors(
            (0,0,0), (43,255,255)
        )
    
    def draw_starter_pokemon(self):
        for index, image in enumerate(self.pokemon_starters_image):
            self.screen.blit(image, (self.width*0.25 * index, self.height*0))