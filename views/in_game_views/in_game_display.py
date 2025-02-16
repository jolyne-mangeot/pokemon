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