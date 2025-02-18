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
        self.load_graphics_combat()

        self.game_state = "player_turn"

        self.forced_switch = False
        self.caught = False
        self.ran_away = False
        self.team_full = False

        self.update_options("battle_stage", True)

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True
        match self.game_state:
            case "start":
                pass
            case "enemy_turn":
                self.enemy_turn_action()
            case "player_turn" | _:
                self.player_turn_action(event)

    def enemy_turn_action(self):
        if random.randint(0,100) > 80:
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
            case "enemy_caught":
                if len(self.battle.player_team) > 6:
                    self.team_full = True
                    self.update_options("display_team")
                else:
                    self.leave_battle()
            case "ran_away":
                self.leave_battle()

    def update(self):
        self.draw()
    
    def draw(self):
        self.draw_action_background()
        self.draw_pokemons()
        
        self.draw_dialogue_box()
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
