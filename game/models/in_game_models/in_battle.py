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
            "enemy_attack": self.pokemon_attack_scene,
            "player_guard": self.pokemon_guard_scene,
            "enemy_guard": self.pokemon_guard_scene,
            "player_idle" : self.pokemon_idle_scene,
            "enemy_idle" : self.pokemon_idle_scene,
            "switch_pokemon_confirmed" : self.pokemon_switch_scene,
            "active_beat": self.pokemon_beat_scene,
            "enemy_beat": self.pokemon_beat_scene,
            "catch_attempt": self.catch_attempt_scene,
            "run_away_attempt": self.run_away_attempt_scene,
            "active_level_up" : self.active_level_up_scene,
            "victory" : self.end_of_battle,
            "defeat" : self.end_of_battle
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
        self.in_battle_musics["wild battle intro"].play()

        self.forced_switch = False
        self.missed = False
        self.caught = False
        self.ran_away = False
        self.ran_away = False
        self.team_full = False
        self.evolved = False

    def cleanup(self):
        """
        cleans up all menu related data
        """
        self.battle.player_pokedex.encounters["done"] +=1
        self.in_battle_musics["wild battle"].stop()
        self.in_battle_musics["victory"].stop()
        self.battle.heal_all()
    
    def leave_battle(self):
        self.battle.check_lost_pokemons()
        self.next = "launch_menu"
        self.done = True

    def enemy_turn_action(self):
        if random.randint(0,100) > 80 + self.battle.enemy_pokemon.level/2:
            self.update_turn("enemy_idle")
        elif random.randint(0,100) < 40 + self.battle.enemy_pokemon.level:
            self.update_turn("enemy_guard")
        else:
            self.update_turn("enemy_attack") 

    def get_event(self, event):
        if self.game_state == "player_turn":
            self.options_states_dict[self.options_states](event)
        else:
            pass

    def update(self):
        if self.game_state == "enemy_turn":
            self.enemy_turn_action()
        self.draw()
    
    def draw(self):
        self.draw_action_background()
        if not self.game_state == "player_turn":
            self.game_state_dict[self.game_state](self.game_state)
        else:
            if self.forced_switch:
                self.draw_enemy_pokemon()
                self.draw_player_pokemon_ground()
                self.draw_pokemons_infos()
            else:
                self.draw_pokemons()
                self.draw_pokemons_infos()
            self.draw_dialogue_box()
            self.draw_options_menu()
