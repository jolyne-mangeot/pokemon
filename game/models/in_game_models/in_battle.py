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

        self.game_state = "start"
        self.init_in_battle_config()
        self.music_channel.play(self.in_battle_musics["wild battle intro"])

        self.forced_switch = False
        self.missed = False
        self.caught = False
        self.ran_away = False
        self.ran_away = False
        self.team_full = False
        self.evolved = False

    def update(self):
        if self.game_state == "enemy_turn":
            self.enemy_turn_action()
        self.draw()

    def cleanup(self):
        """
        cleans up all menu related data
        """
        self.battle.player_pokedex.encounters["done"] +=1
        self.music_channel.stop()
        self.battle.heal_all()

    def start_game_scene(self, none=None):
        """
            Handles player input in the battle stage.
        """
        if not self.enemy_spawn_animation_done:
            if self.animate_spawn(False, False):
                self.play_enemy_pokemon_cry()
                self.enemy_spawn_animation_done = True
                self.animation_frame = 0
            else:
                self.animation_frame +=1
        else:
            if self.animation_frame == 60:
                self.music_channel.play(self.in_battle_musics["wild battle"], -1)
            if self.animate_spawn(True, True):
                self.in_game_actions_sounds["pokemon out"].play()
                self.play_active_pokemon_cry()
                self.end_enemy_turn()
            else:
                self.animation_frame +=1
            
    
    def pokemon_attack_scene(self, attacker="player_attack"):
        if attacker == "player_attack":
            if self.animate_attack(True):
                self.missed = False
                self.end_player_turn()
            else:
                self.animation_frame +=1
                if self.animation_frame == 60:
                    self.efficiency = self.battle.attack(True)
                    if self.efficiency == -1:
                        self.missed = True
                    if self.efficiency >= 2:
                        self.in_game_actions_sounds["hit very effective"].play()
                    elif self.efficiency >=0.5:
                        self.in_game_actions_sounds["hit no effective"].play()
                    else:
                        self.in_game_actions_sounds["hit not very effective"].play()
        else:
            if self.animate_attack(False):
                self.missed = False
                self.end_enemy_turn()
            else:
                self.animation_frame +=1
                if self.animation_frame == 60:
                    self.efficiency = self.battle.attack(False)
                    if self.efficiency == -1:
                        self.missed = True
                    if self.efficiency >= 2:
                        self.in_game_actions_sounds["hit very effective"].play()
                    elif self.efficiency >=0.5:
                        self.in_game_actions_sounds["hit not very effective"].play()
                    else:
                        self.in_game_actions_sounds["hit no effective"].play()
                    if self.battle.active_pokemon.current_health_points <=30:
                        self.in_game_actions_sounds["low health"].play()
    
    def pokemon_guard_scene(self, guarding="player_guard"):
        if self.animation_frame == 1:
            self.in_game_actions_sounds["statup"].play()
        if guarding == "player_guard":
            self.battle.guard(True)
            if self.animate_guard(True):
                self.end_player_turn("guarded")
            else:
                self.animation_frame += 1
        else:
            self.battle.guard(False)
            if self.animate_guard(False):
                self.end_enemy_turn("guarded")
            else:
                self.animation_frame += 1
    
    def pokemon_idle_scene(self, idling="player_idle"):
        if self.animation_frame == 0:
            self.message = random.choice(self.dialogs["idle"])
        if self.animate_pokemon_idling(idling, self.message):
            if idling == "enemy_idle":
                self.end_enemy_turn()
            elif idling == "player_idle":
                self.end_player_turn()
        else:
            self.animation_frame +=1
    
    def pokemon_switch_scene(self, none=None):
        if self.team_full:
            self.battle.player_team.pop(self.chosen_pokemon)
            self.leave_battle()
        else:
            if not self.remove_animation_done:
                if self.forced_switch or self.animate_remove():
                    self.battle.spawn_pokemon(self.chosen_pokemon, True)
                    self.in_game_actions_sounds["pokemon out"].play()
                    self.play_active_pokemon_cry()
                    self.remove_animation_done = True
                    self.animation_frame = 0
                else:
                    self.animation_frame +=1
            elif self.animate_spawn(True, True, True):
                if self.forced_switch:
                    self.update_turn("player_turn")
                    self.update_options("battle_stage")
                else:
                    self.end_player_turn()
                self.forced_switch = False
                self.remove_animation_done = False
            else:
                self.animation_frame +=1
    
    def pokemon_beat_scene(self, beat="active_beat"):
        if beat == "active_beat":
            if self.animate_beat(True):
                if self.battle.check_victory_defeat():
                    self.update_turn("defeat")
                else:
                    self.forced_switch = True
                    self.update_turn("player_turn")
                    self.update_options("display_team")
            else:
                self.animation_frame +=1
        else:
            if self.animate_beat(False):
                self.update_turn("active_level_up")
            else:
                self.animation_frame +=1
    
    def active_level_up_scene(self, none=None):
        if self.animation_frame == 0:
            self.gained_experience = self.battle.gain_experience_all(
                self.put_out_pokemons,
                self.not_put_out_pokemons
            )
        if self.animation_frame == 159:
            level_start = self.battle.active_pokemon.level
            self.battle.level_up_all()
            self.gained_level = self.battle.active_pokemon.level - level_start
            if self.gained_level >=1:
                self.in_game_actions_sounds["levelup"].play()
        if self.animate_level_up():
            if self.battle.check_victory_defeat(self.caught):
                self.update_turn("victory")
            else:
                self.enemy_active_index +=1
                self.battle.spawn_pokemon(self.enemy_active_index, False)
                self.end_enemy_turn()
        else:
            self.animation_frame += 1
    
    def catch_attempt_scene(self, none=None):
        if self.animation_frame == 30 and self.battle.wild:
            self.in_game_actions_sounds["pokeball throw"].play()
        if self.animation_frame == 120 and self.battle.wild:
            self.in_game_actions_sounds["pokeball wobble"].play()
        if self.animation_frame == 360 and self.battle.wild:
            self.caught = self.battle.catch_attempt()
            if self.caught:
                self.music_channel.play(self.in_battle_musics["caught pokemon"])
        if self.animate_catch_attempt():
            if not self.battle.wild:
                self.update_turn("player_turn")
            else:
                if self.caught:
                    self.battle.player_pokedex.catch_pokemon(
                        self.battle.enemy_pokemon.entry, 
                        self.battle.enemy_pokemon.experience_points
                    )
                    self.update_turn("active_level_up")
                else:
                    self.end_player_turn()
        else:
            self.animation_frame +=1
    
    def run_away_attempt_scene(self, none=None):
        if self.animation_frame == 45 and self.battle.wild:
            self.ran_away = self.battle.run_away()
            if self.ran_away:
                self.in_game_actions_sounds["run away"].play()
        if self.animate_run_away():
            if not self.battle.wild:
                self.update_turn("player_turn")
            else:
                if self.ran_away:
                    self.leave_battle()
                else:
                    self.end_player_turn()
        else:
            self.animation_frame +=1
    
    def end_of_battle(self, result="victory"):
        if result == "victory":
            if self.animation_frame == 0:
                self.music_channel.play(self.in_battle_musics["victory"], -1)
            if self.animation_frame == 300:
                self.before_check = self.battle.active_pokemon.name
                self.battle.check_evolutions()
                self.after_check = self.battle.active_pokemon.name
                if self.before_check != self.after_check:
                    self.evolved = True
                    self.music_channel.play(self.in_battle_musics["evolving"])
                if len(self.battle.player_team) > 6:
                    self.team_full = True
            if self.animation_frame == 640 and self.evolved:
                self.load_evolution_combat()
                self.init_evolved_pokemon_cry()
            if self.animation_frame == 675 and self.evolved:
                self.play_active_pokemon_cry()
            if self.animate_victory_message():
                if self.team_full:
                    self.update_turn("player_turn")
                    self.update_options("display_team")
                else:
                    self.leave_battle()
            else:
                self.animation_frame +=1
        else:
            if self.animate_defeat_message():
                self.leave_battle()

    def leave_battle(self):
        self.battle.check_lost_pokemons()
        self.next = "launch_menu"
        self.done = True
