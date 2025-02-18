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
        self.game_dialog_variables : tuple =(
            self.width*0.022,
            self.width*0.07, self.height*0.7
        )
        self.enemy_pokemon_image_size : tuple = (self.width*0.2, self.width*0.2)

        self.active_pokemon_image_coords : tuple = (self.width*0, self.height*0.74 - self.active_pokemon_image_size[0])
        self.enemy_pokemon_image_coords : tuple = (self.width*0.62, self.height*0.08)

        self.active_pokemon_name_coords : tuple = (self.width*0.58, self.height*0.52)
        self.enemy_pokemon_name_coords : tuple = (self.width*0.08, self.height*0.12)

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
        
    def draw_options_menu(self):
        match self.options_states:
            case "battle_stage":
                self.battle_stage_menu.draw_vertical_options()
            case "run_away":
                self.battle_stage_menu.draw_vertical_options()
                self.confirm_action_menu.draw_vertical_options()
            case "display_items":
                self.battle_stage_menu.draw_vertical_options()
                self.display_items_menu.draw_chart_options()
            case "display_team":
                self.battle_stage_menu.draw_vertical_options()
                self.display_team_menu.draw_chart_options()
            case "select_pokemon_confirm":
                self.confirm_action_menu.draw_vertical_options()
    
    def animate_spawn(self, player=True, other_apparent=True):
        if player:
            if self.animation_frame < 90:
                self.screen.blit(
                    self.battle.active_pokemon.back_image,
                    (
                        self.active_pokemon_image_coords[0] - self.width*0.6 + self.width*self.animation_frame/150,
                        self.active_pokemon_image_coords[1]
                    )
                )
                if other_apparent:
                    self.screen.blit(self.battle.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)
                self.blit_dialog(
                    self.dialogs[self.battle.active_pokemon.name] + \
                        self.dialogs["pokemon go"],
                    self.game_dialog_variables[0],
                    self.game_dialog_variables[1],
                    self.game_dialog_variables[2],
                    "bottomleft")
            else:
                return True
        else:
            if self.animation_frame < 120:
                self.screen.blit(
                    self.battle.enemy_pokemon.front_image,
                    (
                        self.enemy_pokemon_image_coords[0] + self.width*1.2 - self.width*self.animation_frame/100,
                        self.enemy_pokemon_image_coords[1]
                    )
                )
                if other_apparent:
                    self.screen.blit(self.battle.active_pokemon.back_image, self.active_pokemon_image_coords)
                self.blit_dialog(
                    self.dialogs["wild appears_1"] + \
                        self.dialogs[self.battle.enemy_pokemon.name] + \
                        self.dialogs["wild appears_2"],
                    self.game_dialog_variables[0],
                    self.game_dialog_variables[1],
                    self.game_dialog_variables[2],
                    "bottomleft")
            else:
                return True

    def animate_attack(self, player=True):
        if player:
            attacker = self.battle.active_pokemon
            attacked = self.battle.enemy_pokemon
        else:
            attacker = self.battle.enemy_pokemon
            attacked = self.battle.active_pokemon
        self.animate_pokemon_attack(player)
        if self.animation_frame < 60:
            self.blit_dialog(
                self.dialogs[attacker.name] + self.dialogs["attacked"],
                self.game_dialog_variables[0],
                self.game_dialog_variables[1],
                self.game_dialog_variables[2],
                "bottomleft")
        elif self.animation_frame < 180:
            self.blit_dialog(
                self.dialogs["effective " + str(self.efficiency)],
                self.game_dialog_variables[0],
                self.game_dialog_variables[1],
                self.game_dialog_variables[2],
                "bottomleft")
        elif self.animation_frame > 180:
            return True

    #self.screen.blit(self.battle.active_pokemon.back_image, self.active_pokemon_image_coords)
    #self.screen.blit(self.battle.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)
    def animate_pokemon_attack(self, player):
        if player:
            if self.animation_frame < 45:
                self.screen.blit(
                    self.battle.active_pokemon.back_image,
                    (
                        self.active_pokemon_image_coords[0],
                        self.active_pokemon_image_coords[1] + (-abs(self.animation_frame) if self.animation_frame < 30 else (self.animation_frame-30)/5)
                    )
                )
                self.screen.blit(self.battle.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)
                self.draw_pokemons_infos()
            elif self.animation_frame < 180:
                self.screen.blit(self.battle.active_pokemon.back_image, self.active_pokemon_image_coords)
                if self.animation_frame not in (60,61,62,63,64,65,80,81,82,83,84,85):
                    self.screen.blit(
                        self.battle.enemy_pokemon.front_image,
                        (
                            self.enemy_pokemon_image_coords[0],
                            self.enemy_pokemon_image_coords[1]
                        )
                    )
                self.draw_pokemons_infos()
            else:
                self.draw_pokemons()
        else:
            if self.animation_frame < 45:
                self.screen.blit(
                    self.battle.enemy_pokemon.front_image,
                    (
                        self.enemy_pokemon_image_coords[0],
                        self.enemy_pokemon_image_coords[1] + (-abs(self.animation_frame) if self.animation_frame < 30 else (self.animation_frame-30)/5)
                    )
                )
                self.screen.blit(self.battle.active_pokemon.back_image, self.active_pokemon_image_coords)
                self.draw_pokemons_infos()
            elif self.animation_frame < 180:
                self.screen.blit(self.battle.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)
                if self.animation_frame not in (60,61,62,63,64,80,81,82,83,84):
                    self.screen.blit(
                        self.battle.active_pokemon.back_image,
                        (
                            self.active_pokemon_image_coords[0],
                            self.active_pokemon_image_coords[1]
                        )
                    )
                self.draw_pokemons_infos()
            else:
                self.draw_pokemons()

    def animate_guard(self, player=True):
        if self.animation_frame < 140:
            self.draw_pokemons()
            self.blit_dialog(
                (self.dialogs[self.battle.active_pokemon.name] if player else self.dialogs[self.battle.enemy_pokemon.name]) + self.dialogs["guarded"],
                self.game_dialog_variables[0],
                self.game_dialog_variables[1],
                self.game_dialog_variables[2],
                "bottomleft")
        else:
            return True