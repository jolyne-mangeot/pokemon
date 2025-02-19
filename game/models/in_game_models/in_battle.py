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
        """
        Initializes the battle state, including menu controllers and battle variables.
        """
        Models_controller.__init__(self)
        Game_menues_controller.__init__(self)
        self.next = "launch_menu"
        self.back = "launch_menu"
        self.event = None
    
    def init_in_battle_config(self):
        self.options_states_dict : dict = {
            "display_items": self.get_event_display_items,
            "display_team": self.get_event_display_team,
            "select_pokemon_confirm": self.get_event_select_pokemon_confirm,
            "run_away": self.get_event_run_away,
            "battle_stage": self.get_event_battle_stage
        }
        self.game_state_dict : dict = {
            "start": self.start_game_scene,
            "player_attack": self.pokemon_attack_scene,
            "player_guard": self.pokemon_guard_scene,
            "enemy_attack": self.pokemon_attack_scene,
            "enemy_guard": self.pokemon_guard_scene,
            "switch_pokemon_confirmed" : self.pokemon_switch_scene,
            "active_beat": self.pokemon_beat_scene,
            "enemy_beat": self.pokemon_beat_scene,
            "catch_attempt": self.catch_attempt_scene,
        }

    def startup(self):
        """
        Initializes battle elements, setting up player and enemy Pokémon.
        """
        self.init_config()
        self.battle = Models_controller.new_battle
        self.init_in_battle_display(self.battle.wild)
        self.init_in_battle_sounds()
        self.not_put_out_pokemons : list = self.battle.player_team.copy()
        self.put_out_pokemons : list = [self.not_put_out_pokemons.pop(0)]
        self.enemy_active_index = 0
        self.battle.spawn_pokemon(self.enemy_active_index, False)
        self.battle.spawn_pokemon(0, True)
        self.animation_frame = 0
        self.enemy_spawn_animation_done = False
        self.player_spawn_animation_done = False
        self.beat_animation_done = False
        self.remove_animation_done = False
        self.load_graphics_combat()

        self.game_state = "start"
        self.init_in_battle_config()

        self.forced_switch = False
        self.caught = False
        self.ran_away = False
        self.ran_away = False
        self.team_full = False

    def cleanup(self):
        """
        cleans up all menu related data
        """
        self.battle.player_pokedex.encounters["done"] +=1
        self.battle.heal_all()
    
    def leave_battle(self):
        self.next = "launch_menu"
        self.done = True

    def enemy_turn_action(self):
        if random.randint(0,100) > 40:
            self.update_turn("enemy_guard")
        else:
            self.update_turn("enemy_attack") 

    def get_event(self, event):
        if self.game_state == "player_turn":
            self.options_states_dict[self.options_states](event)
        else:
            pass

    def update_battle_status(self):
        """
        Updates battle progress by checking Pokémon status and battle outcome
        """
        pokemon_status = self.battle.check_active_pokemon(self.put_out_pokemons, self.not_put_out_pokemons, self.caught)
        end_of_battle = self.battle.check_victory_defeat(self.caught, self.ran_away)
        match pokemon_status:
            case "active_beat":
                if not self.beat_animation_done:
                    self.update_turn("active_beat")
                elif end_of_battle == "defeat":
                    self.leave_battle()
                else:
                    self.forced_switch = True
                    self.game_state = "player_turn"
                    self.update_options("display_team")
                    self.beat_animation_done = False
            case "enemy_beat":
                if not self.beat_animation_done:
                    self.update_turn("enemy_beat")
                elif end_of_battle == "victory":
                    self.battle.check_evolutions()
                    self.leave_battle()
                else:
                    self.enemy_active_index +=1
                    self.battle.spawn_pokemon(self.enemy_active_index, False)
                    self.beat_animation_done = False
        match end_of_battle:
            case "enemy_caught":
                if len(self.battle.player_team) > 5:
                    self.team_full = True
                    self.update_turn("player_turn")
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
        self.draw_action_background()
        try:
            self.game_state_dict[self.game_state](self.game_state)
        except KeyError:
            if self.forced_switch:
                self.draw_enemy_pokemon()
                self.draw_player_pokemon_ground()
                self.draw_pokemons_infos()
            else:
                self.draw_pokemons()
                self.draw_pokemons_infos()
            self.draw_dialogue_box()
            
            self.draw_options_menu()
