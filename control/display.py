import pygame as pg
from assets.__graphics_settings__ import GRAPHICS_PATH
from assets.__fonts_settings__ import FONTS_PATH, POKEMON_CLASSIC_FONT

class Display:
    def __init__(self):
        self.pixel_font = pg.font.Font(FONTS_PATH + POKEMON_CLASSIC_FONT, 20)

    def load_graphics_main_menues(self):
        # self.background = pygame.
        # 
        # 
        pass

    def load_graphics_preferences_menu(self):
        # self.background = 
        pass

    def load_graphics_in_fight(self):
        pass

    def load_graphics_pokemons(self):
        for pokemon in self.fight.player_team:
            pokemon.back_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.back_image)
            pokemon.back_image = pg.transform.scale(pokemon.back_image, (250,250))
        for pokemon in self.fight.enemy_team:
            pokemon.front_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.front_image)
            pokemon.front_image = pg.transform.scale(pokemon.front_image, (150,150))

    def unload_graphics_pokemons(self):
        for pokemon in self.fight.player_team:
            pokemon.get_graphics()
        for pokemon in self.fight.enemy_team:
            pokemon.get_graphics()

    def draw_pokemons(self):
        front_image_rect = self.fight.active_pokemon.back_image.get_rect(bottomleft=(self.screen_rect.width*0.08,self.screen_rect.height*0.65))
        self.screen.blit(self.fight.active_pokemon.back_image,front_image_rect)
        self.screen.blit(self.fight.enemy_pokemon.front_image,(self.screen_rect.width*0.65,self.screen_rect.height*0.22))