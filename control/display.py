import pygame as pg
from assets.__graphics_settings__ import GRAPHICS_PATH

class Display:
    def __init__(self):
        pass

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
            pokemon.back_image = pg.transform.scale(pokemon.back_image, (100,100))
        for pokemon in self.fight.enemy_team:
            pokemon.front_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.front_image)
            pokemon.front_image = pg.transform.scale(pokemon.front_image, (120,120))

    def unload_graphics_pokemons(self):
        for pokemon in self.fight.player_team:
            pokemon.get_graphics()
        for pokemon in self.fight.enemy_team:
            pokemon.get_graphics()

    def draw_pokemons(self):
        self.screen.blit(self.fight.active_pokemon.back_image,(50,300))
        self.screen.blit(self.fight.enemy_pokemon.front_image,(300,60))
    
    def draw_pokemons_health_points(self):
        player_pokemon_bar_rect = (300, 300, 200, 20)
        player_pokemon_health_rect = (300, 300,\
                    self.fight.active_pokemon.current_health_points / self.fight.active_pokemon.health_points *200, 20)
        pg.draw.rect(self.screen, (255,0,0), player_pokemon_bar_rect)
        pg.draw.rect(self.screen, (0,255,0), player_pokemon_health_rect)

        enemy_pokemon_bar_rect = (50, 50, 200, 20)
        enemy_pokemon_health_rect = (50, 50,\
                    self.fight.enemy_pokemon.current_health_points / self.fight.enemy_pokemon.health_points *200, 20)
        pg.draw.rect(self.screen, (255,0,0), enemy_pokemon_bar_rect)
        pg.draw.rect(self.screen, (0,255,0), enemy_pokemon_health_rect)