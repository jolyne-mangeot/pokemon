import pygame as pg
from assets.__graphics_settings__ import GRAPHICS_PATH

class In_fight_display:
    def init_in_fight_display(self, wild):
        self.wild = wild
        self.init_root_variables()
        self.load_graphics_pokemons()

    def init_root_variables(self):
        width : int = self.screen_rect.width
        height : int = self.screen_rect.height

        self.active_pokemon_image_size : tuple = (width*0.3, width*0.3)
        self.enemy_pokemon_image_size : tuple = (width*0.2, width*0.2)

        self.active_pokemon_image_coords : tuple = (width*0, height*0.8 - self.active_pokemon_image_size[0])
        self.enemy_pokemon_image_coords : tuple = (width*0.65, height*0.22)

        self.active_pokemon_name_coords : tuple = (width*0.6, height*0.62)
        self.enemy_pokemon_name_coords : tuple = (width*0.05, height*0.08)

        self.active_pokemon_level_coords : tuple = (
            self.active_pokemon_name_coords[0] + width*0.28,
            self.active_pokemon_name_coords[1])
        self.enemy_pokemon_level_coords : tuple = (
            self.enemy_pokemon_name_coords[0] + width*0.28,
            self.enemy_pokemon_name_coords[1])

        self.health_bar_width : float = width * 0.21
        self.health_bar_height : float = height * 0.02

        self.active_pokemon_hp_coords : tuple = (
            self.active_pokemon_name_coords[0] + width*0.12,
            self.active_pokemon_name_coords[1] + height*0.03)
        self.enemy_pokemon_hp_coords : tuple = (
            self.enemy_pokemon_name_coords[0] + width*0.12,
            self.enemy_pokemon_name_coords[1] + height*0.03)

    def load_graphics_pokemons(self):
        for pokemon in self.fight.player_team:
            pokemon.back_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.back_image)
            pokemon.back_image = pg.transform.scale(pokemon.back_image, self.active_pokemon_image_size)
        for pokemon in self.fight.enemy_team:
            pokemon.front_image = pg.image.load(GRAPHICS_PATH + "pokemon/" + pokemon.front_image)
            pokemon.front_image = pg.transform.scale(pokemon.front_image, self.enemy_pokemon_image_size)

    def unload_graphics_pokemons(self):
        for pokemon in self.fight.player_team:
            pokemon.get_graphics()
        for pokemon in self.fight.enemy_team:
            pokemon.get_graphics()

    def draw_pokemons(self):
        self.screen.blit(self.fight.active_pokemon.back_image, self.active_pokemon_image_coords)
        self.screen.blit(self.fight.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)
        self.draw_pokemons_infos()

    def draw_pokemons_infos(self):
        self.draw_pokemons_names()
        self.draw_pokemons_levels()
        self.draw_pokemons_health_points()
    
    def draw_pokemons_levels(self):
        player_pokemon_level = self.pixel_font.render(self.dialogs["lvl"] + str(self.fight.active_pokemon.level), True, (0,0,0))
        player_pokemon_level_rect = player_pokemon_level.get_rect(bottomleft=(self.active_pokemon_level_coords))
    
        enemy_pokemon_level = self.pixel_font.render(self.dialogs["lvl"] + str(self.fight.enemy_pokemon.level), True, (0,0,0))
        enemy_pokemon_level_rect = enemy_pokemon_level.get_rect(bottomleft=(self.enemy_pokemon_level_coords))

        self.screen.blit(player_pokemon_level, player_pokemon_level_rect)
        self.screen.blit(enemy_pokemon_level, enemy_pokemon_level_rect)
    
    def draw_pokemons_names(self):
        player_pokemon_name = self.pixel_font.render(self.dialogs[self.fight.active_pokemon.name], True, (0,0,0))
        player_pokemon_name_rect = player_pokemon_name.get_rect(bottomleft=self.active_pokemon_name_coords)
    
        enemy_pokemon_name = self.pixel_font.render(
            self.dialogs["wild"] + self.dialogs[self.fight.enemy_pokemon.name] if self.wild and self.language == "en-en" else \
            # self.dialogs[self.fight.enemy_pokemon.name] + self.dialogs["wild"] if self.wild and self.language == "fr-fr" else \
            self.dialogs[self.fight.enemy_pokemon.name],
            True, (0,0,0))
        enemy_pokemon_name_rect = enemy_pokemon_name.get_rect(bottomleft=self.enemy_pokemon_name_coords)

        self.screen.blit(player_pokemon_name, player_pokemon_name_rect)
        self.screen.blit(enemy_pokemon_name, enemy_pokemon_name_rect)
    
    def draw_pokemons_health_points(self):
        player_pokemon_current_hp_rect = (
            self.active_pokemon_hp_coords[0], self.active_pokemon_hp_coords[1],
            self.fight.active_pokemon.current_health_points/self.fight.active_pokemon.health_points * self.health_bar_width,
            self.health_bar_height)

        enemy_pokemon_current_hp_rect = (
            self.enemy_pokemon_hp_coords[0], self.enemy_pokemon_hp_coords[1],
            self.fight.enemy_pokemon.current_health_points/self.fight.enemy_pokemon.health_points * self.health_bar_width,
            self.health_bar_height)

        pg.draw.rect(self.screen, (255,0,0), (self.active_pokemon_hp_coords[0], self.active_pokemon_hp_coords[1],
                                              self.health_bar_width, self.health_bar_height))
        pg.draw.rect(self.screen, (0,255,0), player_pokemon_current_hp_rect)

        pg.draw.rect(self.screen, (255,0,0), (self.enemy_pokemon_hp_coords[0], self.enemy_pokemon_hp_coords[1],
                                              self.health_bar_width, self.health_bar_height))
        pg.draw.rect(self.screen, (0,255,0), enemy_pokemon_current_hp_rect)