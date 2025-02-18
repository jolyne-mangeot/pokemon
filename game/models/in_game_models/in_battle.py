import pygame as pg
import random

from game.control.models_controller import Models_controller
from game.views.in_game_views.in_battle_display import In_battle_display
from game.views.in_game_views.game_menues_sounds import Game_menues_sounds
from game.control.in_game_controllers.game_menues_controller import Game_menues_controller
from game.control.in_game_controllers.in_battle_controller import In_battle_controller

class In_battle(
    Models_controller,
    Game_menues_controller, In_battle_controller, 
    In_battle_display, Game_menues_sounds):

    def __init__(self):
        Models_controller.__init__(self)
        Game_menues_controller.__init__(self)
        self.next = "launch_menu"
        self.back = "launch_menu"

    def cleanup(self):
        """
        cleans up all menu related data
        """
        self.battle.player_pokedex.encounters["done"] +=1
    
    def leave_battle(self):
        self.next = "launch_menu"
        self.done = True

    def startup(self):
        """
        initiates all menu related data
        """
        self.init_config()
        self.battle = Models_controller.new_battle
        self.init_in_battle_display(self.battle.wild)
        self.init_in_game_sounds()
        self.not_put_out_pokemons : list = self.battle.player_team.copy()
        self.put_out_pokemons : list = [self.not_put_out_pokemons.pop(0)]
        self.enemy_active_index = 0
        self.battle.spawn_pokemon(self.enemy_active_index, False)
        self.battle.spawn_pokemon(0, True)
        self.animation_frame = 0
        self.enemy_spawn_animation_done = False
        self.player_spawn_animation_done = False

        self.game_state = "start"

        self.forced_switch = False
        self.caught = False
        self.ran_away = False
        self.ran_away = False
        self.team_full = False

        self.update_options("battle_stage", True)
        self.update_options("battle_stage", True)

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True
        match self.game_state:
            case "enemy_turn":
                pass
            case "player_turn":
                self.player_turn_action(event)
            case _:
                pass

    def enemy_turn_action(self):
        if random.randint(0,100) > 40:
            self.update_turn("enemy_guard")
        else:
            self.update_turn("enemy_attack") 

    def player_turn_action(self, event):
        match self.options_states:
                case "display_items":
                    self.get_event_display_items(event)
                case "display_team":
                    self.get_event_display_team(event)
                case "select_pokemon_confirm":
                    self.get_event_select_pokemon_confirm(event)
                case "run_away":
                    self.get_event_run_away(event)
                case "battle_stage":
                    self.get_event_battle_stage(event)


    def update_battle_status(self):
        pokemon_status = self.battle.check_active_pokemon(self.put_out_pokemons, self.not_put_out_pokemons, self.caught)
        end_of_battle = self.battle.check_victory_defeat(self.caught, self.ran_away)
        match pokemon_status:
            case "active_beat":
                if end_of_battle == "defeat":
                    self.leave_battle()
                else:
                    self.forced_switch = True
                    self.update_options("display_team")
            case "enemy_beat":
                if end_of_battle == "victory":
                    self.battle.check_evolutions()
                    self.leave_battle()
                else:
                    self.enemy_active_index +=1
                    self.battle.spawn_pokemon(self.enemy_active_index, False)
        match end_of_battle:
            case "enemy_caught":
                self.battle.player_pokedex.catch_pokemon(self.battle.enemy_pokemon.entry, self.battle.enemy_pokemon.experience_points)
                if len(self.battle.player_team) > 6:
                    self.team_full = True
                    self.game_state = "player_turn"
                    self.update_options("display_team")
                else:
                    self.leave_battle()
            case "ran_away":
                self.leave_battle()

    def update(self):
        if self.game_state == "enemy_turn":
            self.enemy_turn_action()
        self.draw()
    
    def draw(self):
        self.screen.fill((0,0,255))
        if self.game_state == "player_turn" or self.game_state == "enemy_turn":
            self.draw_pokemons()
        match self.game_state:
            case "start":
                if not self.enemy_spawn_animation_done:
                    if self.animate_spawn(False, False):
                        self.enemy_spawn_animation_done = True
                        self.animation_frame = 0
                    else:
                        self.animation_frame +=1
                elif not self.player_spawn_animation_done:
                    if self.animate_spawn(True, True):
                        self.player_spawn_animation_done = True
                        self.animation_frame = 0
                    else:
                        self.animation_frame +=1
                else:
                    self.end_enemy_turn("player_turn")
            case "player_attack":
                if self.animate_attack(True):
                    self.end_player_turn()
                else:
                    self.animation_frame +=1
                    if self.animation_frame == 60:
                        self.efficiency = self.battle.attack(True)
            case "player_guard":
                if self.animate_guard(True):
                    self.end_player_turn("guarded")
                else:
                    self.animation_frame += 1
            case "enemy_attack":
                if self.animate_attack(False):
                    self.end_enemy_turn()
                else:
                    self.animation_frame +=1
                    if self.animation_frame == 60:
                        self.efficiency = self.battle.attack(False)
            case "enemy_guard":
                if self.animate_guard(False):
                    self.end_enemy_turn("guarded")
                else:
                    self.animation_frame += 1
            case _:
                self.draw_options_menu()