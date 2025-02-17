import pygame as pg
import random

from control.states_control import States
from views.in_game_views.in_fight_display import In_fight_display
from states.in_game_states._game_menu_manager_ import Game_menu_manager
from states.in_game_states._in_fight_states_ import In_fight_states

pg.font.init()

class In_fight(States, Game_menu_manager, In_fight_display, In_fight_states):
    def __init__(self):
        States.__init__(self)
        Game_menu_manager.__init__(self)
        self.next = "launch_menu"
        self.back = "launch_menu"

    def cleanup(self):
        """
        cleans up all menu related data
        """
        self.fight.player_pokedex.encounters["done"] +=1

    def startup(self):
        """
        initiates all menu related data
        """
        self.init_config()
        self.fight = States.new_fight
        self.init_in_fight_display(self.fight.wild)
        self.not_put_out_pokemons : list = self.fight.player_team.copy()
        self.enemy_active_index = 0
        self.fight.spawn_pokemon(0, True)
        self.fight.spawn_pokemon(self.enemy_active_index, False)
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
                            self.fight.player_team.pop(self.chosen_pokemon)
                            self.next = "launch_menu"
                            self.done = True
                            self.selected_index = 0
                        else:
                            self.fight.spawn_pokemon(self.chosen_pokemon, True)
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
            self.fight.attack(False, self.guarded)
        self.guarded = False
        self.enemy_turn = False
        self.update_battle_status()
    
    def update_battle_status(self):
        pokemon_status = self.fight.check_active_pokemon(self.put_out_pokemons, self.not_put_out_pokemons, self.caught)
        end_of_fight = self.fight.check_victory_defeat(self.caught)
        match pokemon_status:
            case "active_beat":
                if end_of_fight == "defeat":
                    self.next = "launch_menu"
                    self.done = True
                    self.selected_index = 0
                else:
                    self.forced_switch = True
                    self.menu_state = "display_team"
                    self.update_options()
                    return "switch"
            case "enemy_beat":
                if end_of_fight == "victory":
                    self.fight.check_evolutions()
                    self.next = "launch_menu"
                    self.done = True
                    self.selected_index = 0
                else:
                    self.enemy_active_index +=1
                    self.fight.spawn_pokemon(self.enemy_active_index, False)
            case "enemy_caught":
                self.fight.player_pokedex.catch_pokemon(self.fight.enemy_pokemon.entry, self.fight.enemy_pokemon.experience_points)
                if len(self.fight.player_team) > 6:
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
