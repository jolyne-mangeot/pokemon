import pygame as pg
import random

from game.control.models_controller import Models_controller
from game.views.in_game_views.in_battle_display import In_battle_display
from game.views.in_game_views.game_menues_sounds import Game_menues_sounds
from game.control.in_game_controllers.game_menues_controller import Game_menues_controller
from game.control.in_game_controllers.in_battle_controller import In_battle_controller

class In_battle(Models_controller, Game_menues_controller, In_battle_controller, In_battle_display, Game_menues_sounds):
    
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

    def startup(self):
        """
        initiates all menu related data
        """
        self.init_config()
        self.battle = Models_controller.new_battle
        self.init_in_battle_display(self.battle.wild)
        self.init_in_game_sounds()
        self.not_put_out_pokemons : list = self.battle.player_team.copy()
        self.enemy_active_index = 0
        self.battle.spawn_pokemon(0, True)
        self.play_active_pokemon_cry()
        self.battle.spawn_pokemon(self.enemy_active_index, False)
        self.put_out_pokemons : list = [self.not_put_out_pokemons.pop(0)]
    
        self.enemy_turn = False
        self.guarded = False
        self.enemy_guarded = False
        self.forced_switch = False
        self.caught = False
        self.team_full = False

        self.menu_state = "battle_stage"
        self.update_options()

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True
        
        if self.enemy_turn:
            self.enemy_turn_action()
        else:
            match self.menu_state:
                case "display_items":
                    self.get_event_display_items(event)
                    if self.caught:
                        self.update_battle_status()
                case "display_team":
                    self.get_event_display_team(event)
                case "select_pokemon_confirm":
                    if self.get_event_select_pokemon_confirm(event):
                        if self.team_full:
                            self.battle.player_team.pop(self.chosen_pokemon)
                            self.next = "launch_menu"
                            self.done = True
                            self.selected_index = 0
                        else:
                            self.battle.spawn_pokemon(self.chosen_pokemon, True)
                            self.forced_switch = False
                            self.enemy_turn = True
                case "run_away":
                    self.get_event_run_away(event)
                case "battle_stage" | _:
                    self.get_event_battle_stage(event)
   
    def enemy_turn_action(self):
        self.update_battle_status()
        if random.randint(0,100) > 80:
            self.enemy_guarded = True
        else:
            self.battle.attack(False, self.guarded)
        self.guarded = False
        self.enemy_turn = False
        self.update_battle_status()
    
    def update_battle_status(self):
        pokemon_status = self.battle.check_active_pokemon(self.put_out_pokemons, self.not_put_out_pokemons, self.caught)
        end_of_battle = self.battle.check_victory_defeat(self.caught)
        match pokemon_status:
            case "active_beat":
                if end_of_battle == "defeat":
                    self.next = "launch_menu"
                    self.done = True
                    self.selected_index = 0
                else:
                    self.forced_switch = True
                    self.menu_state = "display_team"
                    self.update_options()
                    return "switch"
            case "enemy_beat":
                if end_of_battle == "victory":
                    self.battle.check_evolutions()
                    self.next = "launch_menu"
                    self.done = True
                    self.selected_index = 0
                else:
                    self.enemy_active_index +=1
                    self.battle.spawn_pokemon(self.enemy_active_index, False)
            case "enemy_caught":
                self.battle.player_pokedex.catch_pokemon(self.battle.enemy_pokemon.entry, self.battle.enemy_pokemon.experience_points)
                if len(self.battle.player_team) > 6:
                    self.team_full = True
                    self.menu_state = "display_team"
                    self.update_options()
                else:
                    self.next = "launch_menu"
                    self.done = True
                    self.selected_index = 0
        return None

    def update(self):
        self.draw()
    
    def draw(self):
        self.screen.fill((0,0,255))
        self.draw_pokemons()
        match self.menu_state:
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
                self.battle_stage_menu.draw_vertical_options()
                self.confirm_action_menu.draw_vertical_options()
                self.display_team_menu.draw_chart_options()
