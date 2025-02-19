import pygame as pg

from game.views.in_game_views.game_menues_display import Game_menues_display
from game.models.menu_models.option_menu_model import Option_menu_model

class In_battle_display(Game_menues_display):
    """
        This class represents the display settings and behavior during a battle in the game.
    """
    def init_in_battle_display(self, wild):
        """
        Initializes the battle display
        """
        self.init_in_game_display()
        self.wild = wild
        self.init_root_variables_in_battle()
        self.init_menues_objects()
        self.enemy_pokemon_load()
        self.load_pkmn_info_box()


    def init_root_variables_in_battle(self):
        """
            Sets up the root variables used specifically for battle, such as menu dimensions,
            Pokémon image sizes, coordinates for displaying health bars, names, and levels.
        """
        self.init_root_variables_in_game()

        self.battle_stage_menu_variables : tuple = (
            self.width*0.8, self.height*0.69, 38
        )
        self.confirm_menu_variables : tuple = (
            self.width*0.8, self.height*0.83, 42
        )
        self.display_team_variables : tuple = (
            self.width*0.3, self.height*0.74, 30
        )
        self.game_dialog_variables : tuple =(
            self.width*0.024,
            self.width*0.06, self.height*0.76,
            "bottomleft", (255,255,255), True
        )
        self.enemy_pokemon_image_size : tuple = (
            self.width*0.2, self.width*0.2
        )
        self.active_pokemon_image_coords : tuple = (
            self.width*0, 
            self.height*0.74 - self.active_pokemon_image_size[0]
        )
        self.enemy_pokemon_image_coords : tuple = (
            self.width*0.62, self.height*0.08
        )
        self.enemy_pokemon_ground_multiplicator : tuple = (
            self.width*-abs(0.05),
            self.height*0.15
        )
        self.active_pokemon_ground_multiplicator : tuple = (
            self.width*-abs(0.1),
            self.height*0.22
        )
        self.enemy_pokemon_ground_coords : tuple =(
            self.enemy_pokemon_image_coords[0] +\
                self.enemy_pokemon_ground_multiplicator[0],
            self.enemy_pokemon_image_coords[1] +\
                self.enemy_pokemon_ground_multiplicator[1]
        )
        self.active_pokemon_ground_coords : tuple =(
            self.active_pokemon_image_coords[0] +\
                self.active_pokemon_ground_multiplicator[0],
            self.active_pokemon_image_coords[1] +\
                self.active_pokemon_ground_multiplicator[1]
        )
        self.active_pokemon_name_coords : tuple = (
            self.width*0.588, self.height*0.505
        )
        self.enemy_pokemon_name_coords : tuple = (
            self.width*0.08, self.height*0.09
        )

        self.active_pokemon_level_coords : tuple = (
            self.active_pokemon_name_coords[0] + self.width*0.29,
            self.active_pokemon_name_coords[1]
        )
        self.enemy_pokemon_level_coords : tuple = (
            self.enemy_pokemon_name_coords[0] + self.width*0.29,
            self.enemy_pokemon_name_coords[1]
        )
        self.health_bar_width : float = self.width * 0.23
        self.health_bar_height : float = self.height * 0.02

        self.active_pokemon_health_bar_coords : tuple = (
            self.active_pokemon_name_coords[0] + self.width*0.12,
            self.active_pokemon_name_coords[1] + self.height*0.03
        )
        self.enemy_pokemon_health_bar_coords : tuple = (
            self.enemy_pokemon_name_coords[0] + self.width*0.12,
            self.enemy_pokemon_name_coords[1] + self.height*0.03
        )
        self.active_pokemon_health_points_coords : tuple = (
            self.active_pokemon_name_coords[0] + self.width*0.33, 
            self.active_pokemon_name_coords[1] + self.height*0.05
        )
    
    def init_menues_objects(self):
        """
            Initializes the various menu objects for the battle stage, such as the main action menu,
            confirmation menu, items menu, and team menu.
        """
        self.battle_stage_menu = Option_menu_model(
            self.battle_stage_menu_variables,
            [
                self.dialogs["attack"],
                self.dialogs["guard"],
                self.dialogs["team"],
                self.dialogs["items"],
                self.dialogs["run away"]
            ],
            ["", "", "display_team", "display_items", "run_away"],
            deselected_color=(0,0,0),
            selected_color=(48,84,109)
        )
        self.confirm_action_menu = Option_menu_model(
            self.confirm_menu_variables,
            [self.dialogs["yes"], self.dialogs["no"]],
            deselected_color=(255,255,255),
            selected_color=(248,232,0)
        )
        self.display_items_menu = Option_menu_model(
            self.display_team_variables,
            ["pokeball", "potion", self.dialogs["back"]],
            deselected_color=(255,255,255),
            selected_color=(248,232,0)
        )
        self.display_team_menu = Option_menu_model(
            self.display_team_variables,
            self.init_render_option_team(self.battle.player_team),
            deselected_color=(255,255,255),
            selected_color=(248,232,0)
        )
        self.select_pokemon_confirm_menu = Option_menu_model(
            self.confirm_menu_variables,
            [self.dialogs["no"], self.dialogs["yes"]],
            deselected_color=(255,255,255),
            selected_color=(248,232,0)
        )

    def enemy_pokemon_load(self):
        """
            Loads and scales the front-facing images for the enemy Pokémon team.
            Images are loaded from the specified path and resized to fit the defined dimensions.
        """
        for pokemon in self.battle.enemy_team:
            front_image = pg.image.load(self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/front.png")
            pokemon.front_image = pg.transform.scale(front_image, self.enemy_pokemon_image_size)

    def draw_pokemons(self):
        self.screen.blit(self.active_pokemon_ground_img, self.active_pokemon_ground_coords)
        self.screen.blit(self.pokemon_ground_img, self.enemy_pokemon_ground_coords)
        self.screen.blit(self.battle.active_pokemon.back_image, self.active_pokemon_image_coords)
        self.screen.blit(self.battle.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)
    
    def draw_player_pokemon(self):
        self.screen.blit(self.active_pokemon_ground_img, self.active_pokemon_ground_coords)
        self.screen.blit(self.battle.active_pokemon.back_image, self.active_pokemon_image_coords)
    def draw_enemy_pokemon(self):
        self.screen.blit(self.pokemon_ground_img, self.enemy_pokemon_ground_coords)
        self.screen.blit(self.battle.enemy_pokemon.front_image, self.enemy_pokemon_image_coords)

    def draw_player_pokemon_ground(self):
        self.screen.blit(self.active_pokemon_ground_img, self.active_pokemon_ground_coords)
    def draw_enemy_pokemon_ground(self):
        self.screen.blit(self.pokemon_ground_img, self.enemy_pokemon_ground_coords)

    def draw_pokemons_infos(self):
        self.draw_pkmn_info_box_enemy()
        self.draw_pkmn_info_box_player()
        self.draw_pokemons_names()
        self.draw_pokemons_levels()
        self.draw_pokemons_health_points()
    
    def draw_pokemons_levels(self):
        """
            Renders the levels of both the player's and enemy's Pokémon and displays them on the screen.
        """
        player_pokemon_level = self.pixel_font_pokemon_infos.render(self.dialogs["lvl"] + str(self.battle.active_pokemon.level), True, (0,0,0))
        player_pokemon_level_rect = player_pokemon_level.get_rect(bottomleft=(self.active_pokemon_level_coords))
    
        enemy_pokemon_level = self.pixel_font_pokemon_infos.render(self.dialogs["lvl"] + str(self.battle.enemy_pokemon.level), True, (0,0,0))
        enemy_pokemon_level_rect = enemy_pokemon_level.get_rect(bottomleft=(self.enemy_pokemon_level_coords))

        self.screen.blit(player_pokemon_level, player_pokemon_level_rect)
        self.screen.blit(enemy_pokemon_level, enemy_pokemon_level_rect)
    
    def draw_pokemons_names(self):
        """
            Renders the names of both the player's and enemy's Pokémon, handling different cases for wild Pokémon
        """
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
        """
            Draws the health points of both the player's and enemy's Pokémon using green bars
            that decrease based on the current health relative to max health.
        """
        player_pokemon_current_hp_rect = (
            self.active_pokemon_health_bar_coords[0], self.active_pokemon_health_bar_coords[1],
            self.battle.active_pokemon.current_health_points/self.battle.active_pokemon.health_points * self.health_bar_width,
            self.health_bar_height)

        enemy_pokemon_current_hp_rect = (
            self.enemy_pokemon_health_bar_coords[0], self.enemy_pokemon_health_bar_coords[1],
            self.battle.enemy_pokemon.current_health_points/self.battle.enemy_pokemon.health_points * self.health_bar_width,
            self.health_bar_height)
        
        player_pokemon_health_print = self.pixel_font_pokemon_infos.render(
            (str(int(self.battle.active_pokemon.current_health_points)) + "/" + str(int(self.battle.active_pokemon.health_points))), True, (0,0,0))
        player_pokemon_health_rect = player_pokemon_health_print.get_rect(topright=self.active_pokemon_health_points_coords)
        self.screen.blit(player_pokemon_health_print, player_pokemon_health_rect)

        pg.draw.rect(self.screen, (255,0,0), (self.active_pokemon_health_bar_coords[0], self.active_pokemon_health_bar_coords[1],
                                            self.health_bar_width, self.health_bar_height))
        pg.draw.rect(self.screen, (255,0,0), (self.enemy_pokemon_health_bar_coords[0], self.enemy_pokemon_health_bar_coords[1],
                                            self.health_bar_width, self.health_bar_height))
        pg.draw.rect(self.screen, (0,255,0), player_pokemon_current_hp_rect)
        pg.draw.rect(self.screen, (0,255,0), enemy_pokemon_current_hp_rect)
        
    def draw_options_menu(self):
        match self.options_states:
            case "battle_stage":
                self.draw_action_box()
                self.blit_dialog(
                    self.dialogs["what to do_1"] +\
                    self.battle.player_pokedex.player +\
                    self.dialogs["what to do_2"],
                    *self.game_dialog_variables
                )
                self.battle_stage_menu.draw_vertical_options()
            case "run_away":
                self.blit_dialog(
                    self.dialogs["run away proceed"],
                    *self.game_dialog_variables
                )
                self.confirm_action_menu.draw_vertical_options()
            case "display_items":
                self.display_items_menu.draw_chart_options()
            case "display_team":
                self.display_team_menu.draw_chart_options()
            case "select_pokemon_confirm":
                self.blit_dialog_select_pokemon()
                self.confirm_action_menu.draw_vertical_options()
    
    def blit_dialog_select_pokemon(self):
        if self.team_full:
            self.blit_dialog(
                self.dialogs["let pokemon go"] +\
                self.dialogs[self.battle.player_team[self.chosen_pokemon].name] +\
                self.dialogs["?"],
                *self.game_dialog_variables
            )
        else:
            self.blit_dialog(
                self.dialogs["send pokemon_1"] +\
                self.dialogs[self.battle.player_team[self.chosen_pokemon].name] +\
                self.dialogs["send pokemon_2"],
                *self.game_dialog_variables
            )

    def animate_spawn(self, player=True, other_apparent=True, infos_apparent=False):
        if player:
            if self.animation_frame < 90:
                pokemon_coords=(
                    self.active_pokemon_image_coords[0] - self.width*0.6 + self.width*self.animation_frame/150,
                    self.active_pokemon_image_coords[1]
                )
                self.draw_player_pokemon_ground()
                self.screen.blit(
                    self.battle.active_pokemon.back_image,
                    pokemon_coords
                )
                if other_apparent:
                    self.draw_enemy_pokemon()
                if infos_apparent:
                    self.draw_pokemons_infos()
                self.draw_dialogue_box()
                self.blit_dialog(
                        self.dialogs[self.battle.active_pokemon.name] + \
                        self.dialogs["pokemon go"],
                        *self.game_dialog_variables
                    )
            else:
                return True
        else:
            if self.animation_frame < 120:
                pokemon_coords=(
                    self.enemy_pokemon_image_coords[0] + self.width*1.2 - self.width*self.animation_frame/100,
                    self.enemy_pokemon_image_coords[1]
                )
                self.screen.blit(
                    self.pokemon_ground_img,
                    (
                        pokemon_coords[0] +\
                        self.enemy_pokemon_ground_multiplicator[0],
                        pokemon_coords[1] +\
                        self.enemy_pokemon_ground_multiplicator[1]
                    )
                )
                self.screen.blit(
                    self.battle.enemy_pokemon.front_image,
                    pokemon_coords
                )
                if infos_apparent:
                    self.draw_pokemons_infos()
                if other_apparent:
                    self.draw_player_pokemon()
                else:
                    self.draw_player_pokemon_ground()
                self.draw_dialogue_box()
                self.blit_dialog(
                    self.dialogs["wild appears_1"] + \
                    self.dialogs[self.battle.enemy_pokemon.name] + \
                    self.dialogs["wild appears_2"],
                    *self.game_dialog_variables
                )
            else:
                return True
    
    def animate_remove(self):
        if self.animation_frame < 50:
            self.draw_player_pokemon_ground()
            pokemon_coords = (
                self.active_pokemon_image_coords[0] - self.animation_frame*2,
                self.active_pokemon_image_coords[1]
            )
            self.screen.blit(
                self.battle.active_pokemon.back_image,
                pokemon_coords
            )
            self.draw_enemy_pokemon()
            self.draw_pokemons_infos()
            self.draw_dialogue_box()
            self.blit_dialog(
                self.dialogs[self.battle.active_pokemon.name] +\
                self.dialogs["come back"],
                *self.game_dialog_variables
            )
            return False
        else:
            return True
    
    def animate_beat(self, player=True):
        if self.animation_frame < 90:
            self.animate_pokemon_beat(player)
            self.draw_pokemons_infos()
            self.draw_dialogue_box()
            self.blit_dialog(
                (self.dialogs["active beat_1"] +\
                self.dialogs[self.battle.active_pokemon.name] +\
                self.dialogs["active beat_2"] if player else\
                self.dialogs["enemy beat_1"] +\
                self.dialogs[self.battle.enemy_pokemon.name] +\
                self.dialogs["enemy beat_2"]),
                *self.game_dialog_variables
            )
            return False
        else:
            return True

    def animate_pokemon_beat(self, player=True):
        if player:
            self.draw_player_pokemon_ground()
            if self.animation_frame < 45:
                pokemon_coords=(
                    self.active_pokemon_image_coords[0],
                    self.active_pokemon_image_coords[1] + self.width*self.animation_frame/100
                )
                self.screen.blit(
                    self.battle.active_pokemon.back_image,
                    pokemon_coords
                )
            self.draw_enemy_pokemon()
        else:
            if self.animation_frame < 45:
                pokemon_coords=(
                    self.enemy_pokemon_image_coords[0],
                    self.enemy_pokemon_image_coords[1] + self.width*self.animation_frame/100
                )
                self.draw_enemy_pokemon_ground()
                self.screen.blit(
                    self.battle.enemy_pokemon.front_image,
                    pokemon_coords
                )
            self.draw_player_pokemon()
    
    def animate_attack(self, player=True):
        if player:
            attacker = self.battle.active_pokemon
            attacked = self.battle.enemy_pokemon
        else:
            attacker = self.battle.enemy_pokemon
            attacked = self.battle.active_pokemon
        self.animate_pokemon_attack(player)
        if self.animation_frame < 60:
            self.draw_dialogue_box()
            self.blit_dialog(
                self.dialogs[attacker.name] + self.dialogs["pokemon attack"],
                *self.game_dialog_variables)
        elif self.animation_frame < 150:
            self.draw_dialogue_box()
            self.blit_dialog(
                self.dialogs["effective " + str(self.efficiency)],
                *self.game_dialog_variables)
        elif self.animation_frame > 150:
            return True

    def animate_pokemon_attack(self, player):
        if player:
            if self.animation_frame < 45:
                pokemon_coords=(
                    self.active_pokemon_image_coords[0],
                    self.active_pokemon_image_coords[1] + (-abs(self.animation_frame) if self.animation_frame < 30 else (self.animation_frame-30)/5)
                )
                self.draw_player_pokemon_ground()
                self.screen.blit(
                    self.battle.active_pokemon.back_image,
                    pokemon_coords
                )
                self.draw_enemy_pokemon()
                self.draw_pokemons_infos()
            elif self.animation_frame < 150:
                self.draw_player_pokemon()
                self.draw_enemy_pokemon_ground()
                if self.animation_frame not in (60,61,62,63,70,71,72,73):
                    self.draw_enemy_pokemon()
                self.draw_pokemons_infos()
            else:
                self.draw_pokemons()
                self.draw_pokemons_infos()
        else:
            if self.animation_frame < 45:
                pokemon_coords=(
                    self.enemy_pokemon_image_coords[0],
                    self.enemy_pokemon_image_coords[1] + (-abs(self.animation_frame) if self.animation_frame < 30 else (self.animation_frame-30)/5)
                )
                self.draw_enemy_pokemon_ground()
                self.screen.blit(
                    self.battle.enemy_pokemon.front_image,
                    pokemon_coords
                )
                self.draw_player_pokemon()
                self.draw_pokemons_infos()
            elif self.animation_frame < 180:
                self.draw_enemy_pokemon()
                self.draw_player_pokemon_ground()
                if self.animation_frame not in (60,61,62,63,70,71,72,73):
                    self.draw_player_pokemon()
                self.draw_pokemons_infos()
            else:
                self.draw_pokemons()
                self.draw_pokemons_infos()

    def animate_guard(self, player=True):
        if self.animation_frame < 140:
            self.draw_pokemons()
            self.draw_pokemons_infos()
            self.draw_dialogue_box()
            self.blit_dialog(
                (self.dialogs[self.battle.active_pokemon.name] if player\
                else self.dialogs[self.battle.enemy_pokemon.name]) + \
                self.dialogs["guarded"],
                *self.game_dialog_variables)
        else:
            return True
    
    def animate_catch_attempt(self):
        if self.battle.wild:
            if self.animation_frame < 270:
                if self.animation_frame < 45:
                    self.draw_pokemons()
                if 45 < self.animation_frame < 150:
                    self.draw_player_pokemon()
                    self.draw_enemy_pokemon_ground()
                    self.draw_pokeball_thrown()
                else:
                    if self.caught:
                        self.draw_player_pokemon()
                        self.draw_enemy_pokemon_ground()
                        self.draw_pokeball_caught()
                    else:
                        self.draw_pokemons()
                self.draw_pokemons_infos()
                self.draw_dialogue_box()
                if self.animation_frame < 150:
                    self.blit_dialog(
                        self.battle.player_pokedex.player +\
                        self.dialogs["catch attempt"],
                        *self.game_dialog_variables
                    )
                else:
                    if self.caught:
                        self.blit_dialog(
                            self.dialogs["caught pokemon_1"] +\
                            self.dialogs[self.battle.enemy_pokemon.name] +\
                            self.dialogs["caught pokemon_2"],
                            *self.game_dialog_variables
                        )
                    else:
                        self.blit_dialog(
                            self.dialogs["broke free"],
                            *self.game_dialog_variables
                        )
            if self.animation_frame > 270:
                return True
            else:
                return False
        elif not self.battle.wild:
            self.draw_pokemons()
            self.draw_pokemons_infos()
            self.draw_dialogue_box()
            self.blit_dialog(
                self.dialogs["not catchable"],
                *self.game_dialog_variables
            )
            if self.animation_frame > 45:
                return True
            else:
                return False

    def animate_run_away(self):
        pass