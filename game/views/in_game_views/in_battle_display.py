import pygame as pg

from game.views.in_game_views.game_menues_display import Game_menues_display
from game.models.menu_models.option_menu_model import Option_menu_model

class In_battle_display(Game_menues_display):
    def init_in_battle_display(self, wild):
        self.init_in_game_display()
        self.wild = wild
        self.init_root_variables_in_battle()
        self.init_menues_objects()
        self.enemy_pokemon_load()

    def init_root_variables_in_battle(self):
        self.init_root_variables_in_game()

        self.battle_stage_menu_variables : tuple = (
            self.width*0.8, self.height*0.72, 38
        )
        self.confirm_menu_variables : tuple = (
            self.width*0.6, self.height*0.9, 38
        )
        self.display_team_variables : tuple = (
            self.width*0.2, self.height*0.78, 38
        )
        self.enemy_pokemon_image_size : tuple = (self.width*0.2, self.width*0.2)

        self.active_pokemon_image_coords : tuple = (self.width*0, self.height*0.778 - self.active_pokemon_image_size[0])
        self.enemy_pokemon_image_coords : tuple = (self.width*0.65, self.height*0.22)

        self.active_pokemon_name_coords : tuple = (self.width*0.58, self.height*0.58)
        self.enemy_pokemon_name_coords : tuple = (self.width*0.05, self.height*0.08)

        self.active_pokemon_level_coords : tuple = (
            self.active_pokemon_name_coords[0] + self.width*0.28,
            self.active_pokemon_name_coords[1])
        self.enemy_pokemon_level_coords : tuple = (
            self.enemy_pokemon_name_coords[0] + self.width*0.28,
            self.enemy_pokemon_name_coords[1])

        self.health_bar_width : float = self.width * 0.21
        self.health_bar_height : float = self.height * 0.02

        self.active_pokemon_hb_coords : tuple = (
            self.active_pokemon_name_coords[0] + self.width*0.12,
            self.active_pokemon_name_coords[1] + self.height*0.03)
        self.enemy_pokemon_hb_coords : tuple = (
            self.enemy_pokemon_name_coords[0] + self.width*0.12,
            self.enemy_pokemon_name_coords[1] + self.height*0.03)
        
        self.active_pokemon_hp_coords : tuple = (
            self.active_pokemon_name_coords[0] + self.width*0.33, 
            self.active_pokemon_name_coords[1] + self.height*0.05)
    
    def init_menues_objects(self):
        self.battle_stage_menu = Option_menu_model(
            self.battle_stage_menu_variables,
            [
                self.dialogs["attack"],
                self.dialogs["guard"],
                self.dialogs["team"],
                self.dialogs["items"],
                self.dialogs["run away"]
            ],
            ["", "", "display_team", "display_items", "run_away"]
        )
        self.confirm_action_menu = Option_menu_model(
            self.confirm_menu_variables,
            [self.dialogs["no"], self.dialogs["yes"]],
        )
        self.display_items_menu = Option_menu_model(
            self.display_team_variables,
            ["pokeball", "potion", self.dialogs["back"]]
        )
        self.display_team_menu = Option_menu_model(
            self.display_team_variables,
            self.init_render_option_team(self.battle.player_team)
        )
        self.select_pokemon_confirm_menu = Option_menu_model(
            self.confirm_menu_variables,
            [self.dialogs["no"], self.dialogs["yes"]]
        )

    def enemy_pokemon_load(self):
        for pokemon in self.battle.enemy_team:
            front_image = pg.image.load(self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/front.png")
            pokemon.front_image = pg.transform.scale(front_image, self.enemy_pokemon_image_size)

    def draw_pokemons(self):
        self.screen.blit(self.battle.active_pokemon.back_image, self.active_pokemon_image_coords)
        self.screen.blit(self.battle.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)
        self.draw_pokemons_infos()

    def draw_pokemons_infos(self):
        self.draw_pokemons_names()
        self.draw_pokemons_levels()
        self.draw_pokemons_health_points()
    
    def draw_pokemons_levels(self):
        player_pokemon_level = self.pixel_font_pokemon_infos.render(self.dialogs["lvl"] + str(self.battle.active_pokemon.level), True, (0,0,0))
        player_pokemon_level_rect = player_pokemon_level.get_rect(bottomleft=(self.active_pokemon_level_coords))
    
        enemy_pokemon_level = self.pixel_font_pokemon_infos.render(self.dialogs["lvl"] + str(self.battle.enemy_pokemon.level), True, (0,0,0))
        enemy_pokemon_level_rect = enemy_pokemon_level.get_rect(bottomleft=(self.enemy_pokemon_level_coords))

        self.screen.blit(player_pokemon_level, player_pokemon_level_rect)
        self.screen.blit(enemy_pokemon_level, enemy_pokemon_level_rect)
    
    def draw_pokemons_names(self):
        player_pokemon_name = self.pixel_font_pokemon_infos.render(self.dialogs[self.battle.active_pokemon.name], True, (0,0,0))
        player_pokemon_name_rect = player_pokemon_name.get_rect(bottomleft=self.active_pokemon_name_coords)
    
        enemy_pokemon_name = self.pixel_font_pokemon_infos.render(
            self.dialogs["wild"] + self.dialogs[self.battle.enemy_pokemon.name] if self.wild and self.language == "en-en" else \
            # self.dialogs[self.battle.enemy_pokemon.name] + self.dialogs["wild"] if self.wild and self.language == "fr-fr" else \
            self.dialogs[self.battle.enemy_pokemon.name],
            True, (0,0,0))
        enemy_pokemon_name_rect = enemy_pokemon_name.get_rect(bottomleft=self.enemy_pokemon_name_coords)

        self.screen.blit(player_pokemon_name, player_pokemon_name_rect)
        self.screen.blit(enemy_pokemon_name, enemy_pokemon_name_rect)
    
    def draw_pokemons_health_points(self):
        player_pokemon_current_hp_rect = (
            self.active_pokemon_hb_coords[0], self.active_pokemon_hb_coords[1],
            self.battle.active_pokemon.current_health_points/self.battle.active_pokemon.health_points * self.health_bar_width,
            self.health_bar_height)

        enemy_pokemon_current_hp_rect = (
            self.enemy_pokemon_hb_coords[0], self.enemy_pokemon_hb_coords[1],
            self.battle.enemy_pokemon.current_health_points/self.battle.enemy_pokemon.health_points * self.health_bar_width,
            self.health_bar_height)
        
        player_pokemon_health_print = self.pixel_font_pokemon_infos.render(
            (str(int(self.battle.active_pokemon.current_health_points)) + "/" + str(int(self.battle.active_pokemon.health_points))), True, (0,0,0))
        player_pokemon_health_rect = player_pokemon_health_print.get_rect(topright=self.active_pokemon_hp_coords)
        self.screen.blit(player_pokemon_health_print, player_pokemon_health_rect)

        pg.draw.rect(self.screen, (255,0,0), (self.active_pokemon_hb_coords[0], self.active_pokemon_hb_coords[1],
                                            self.health_bar_width, self.health_bar_height))
        pg.draw.rect(self.screen, (255,0,0), (self.enemy_pokemon_hb_coords[0], self.enemy_pokemon_hb_coords[1],
                                            self.health_bar_width, self.health_bar_height))
        pg.draw.rect(self.screen, (0,255,0), player_pokemon_current_hp_rect)
        pg.draw.rect(self.screen, (0,255,0), enemy_pokemon_current_hp_rect)
        
        