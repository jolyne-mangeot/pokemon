import pygame as pg
from assets.__graphics_settings__ import GRAPHICS_PATH
from assets.__fonts_settings__ import FONTS_PATH, POKEMON_CLASSIC_FONT

class Display:
    def __init__(self):
        self.pixel_font = pg.font.Font(FONTS_PATH + POKEMON_CLASSIC_FONT, int(self.screen_rect.width*0.02))

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
            pokemon.back_image = pg.transform.scale(pokemon.back_image, (self.screen_rect.width*0.3,self.screen_rect.width*0.3))
        for pokemon in self.fight.enemy_team:
            pokemon.front_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.front_image)
            pokemon.front_image = pg.transform.scale(pokemon.front_image, (self.screen_rect.width*0.2,self.screen_rect.width*0.2))

    def unload_graphics_pokemons(self):
        for pokemon in self.fight.player_team:
            pokemon.get_graphics()
        for pokemon in self.fight.enemy_team:
            pokemon.get_graphics()

    def draw_pokemons(self):
        back_image_rect = self.fight.active_pokemon.back_image.get_rect(bottomleft=(self.screen_rect.width*0,self.screen_rect.height*0.8))
        self.screen.blit(self.fight.active_pokemon.back_image, back_image_rect)
        self.screen.blit(self.fight.enemy_pokemon.front_image, (self.screen_rect.width*0.65,self.screen_rect.height*0.22))

    def draw_pokemons_infos(self):
        player_pokemon_name = self.pixel_font.render(self.fight.active_pokemon.name, 1, (0,0,0))
        player_pokemon_name_rect = player_pokemon_name.get_rect(bottomleft=(self.screen_rect.width*0.58,self.screen_rect.height*0.62))
    
        enemy_pokemon_name = self.pixel_font.render(self.fight.enemy_pokemon.name, 1, (0,0,0))
        enemy_pokemon_name_rect = enemy_pokemon_name.get_rect(bottomleft=(self.screen_rect.width*0.05, self.screen_rect.height*0.08))

        self.screen.blit(player_pokemon_name, player_pokemon_name_rect)
        self.screen.blit(enemy_pokemon_name, enemy_pokemon_name_rect)
    
    def draw_pokemons_health_points(self):
        player_pokemon_bar_rect = (self.screen_rect.width*0.65, self.screen_rect.height*0.65, 200, 20)
        player_pokemon_health_rect = (self.screen_rect.width*0.65, self.screen_rect.height*0.65,\
                    self.fight.active_pokemon.current_health_points / self.fight.active_pokemon.health_points *200, 20)
        pg.draw.rect(self.screen, (255,0,0), player_pokemon_bar_rect)
        pg.draw.rect(self.screen, (0,255,0), player_pokemon_health_rect)

        enemy_pokemon_bar_rect = (self.screen_rect.width*0.15, self.screen_rect.height*0.1, 200, 20)
        enemy_pokemon_health_rect = (self.screen_rect.width*0.15, self.screen_rect.height*0.1,\
                    self.fight.enemy_pokemon.current_health_points / self.fight.enemy_pokemon.health_points *200, 20)
        pg.draw.rect(self.screen, (255,0,0), enemy_pokemon_bar_rect)
        pg.draw.rect(self.screen, (0,255,0), enemy_pokemon_health_rect)