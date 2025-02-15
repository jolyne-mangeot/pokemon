import pygame as pg
import random
from control.states_control import States
from states.in_game_states.__game_menu_manager__ import Game_menu_manager
from states.in_game_states.__in_fight_states__ import In_fight_states

pg.font.init()

class In_fight(States, Game_menu_manager, In_fight_states):
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
        self.unload_graphics_pokemons()

    def startup(self):
        """
        initiates all menu related data
        """
        self.init_config()
        self.fight = States.new_fight
        self.menu_state = "battle_stage"
        self.update_options()
        self.not_put_out_pokemons : list = self.fight.player_team.copy()
        self.fight.spawn_pokemon(0, True)
        self.enemy_active_index = 0
        self.fight.spawn_pokemon(self.enemy_active_index, False)
        self.put_out_pokemons : list = [self.not_put_out_pokemons.pop(0)]
        self.init_in_fight_display(self.fight.wild)
        self.enemy_turn = False
        self.guarded = False
        self.enemy_guarded = False
        self.forced_switch = False

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
                # case "display_items":
                #     self.get_event_display_items(event)
                #     self.get_event_menu(event)
                case "display_team":
                    self.get_event_display_team(event)
                    self.get_event_menu(event)
                case "select_pokemon_confirm":
                    if self.get_event_select_pokemon_confirm(event):
                        self.fight.spawn_pokemon(self.chosen_pokemon, True)
                        self.forced_switch = False
                        self.enemy_turn = True
                    self.get_event_menu(event)
                case "quit":
                    self.back = "battle_stage"
                    self.get_event_run_away(event)
                    self.get_event_menu(event)
                case "battle_stage" | _:
                    self.get_event_battle_stage(event)
                    self.get_event_menu(event)
   
    def enemy_turn_action(self):
        if random.randint(0,100) > 80:
            self.enemy_guarded = True
        else:
            self.fight.attack(False, self.guarded)
        self.guarded = False
        self.enemy_turn = False
        self.update_battle_status()
    
    def update_battle_status(self):
        pokemon_status = self.fight.check_active_pokemon(self.put_out_pokemons, self.not_put_out_pokemons)
        end_of_fight = self.fight.check_victory_defeat()
        if pokemon_status == "active_beat":
            if end_of_fight == "defeat":
                self.next = "launch_menu"
                self.done = True
                self.selected_index = 0
            else:
                self.forced_switch = True
                self.menu_state = "display_team"
                self.update_options()
                return "switch"
        elif pokemon_status == "enemy_beat":
            if end_of_fight == "victory":
                self.fight.check_evolutions()
                self.next = "launch_menu"
                self.done = True
                self.selected_index = 0
            else:
                self.enemy_active_index +=1
                self.fight.spawn_pokemon(self.enemy_active_index, False)
        return None

    def update(self):
        self.draw()
    
    def draw(self):
        self.screen.fill((0,0,255))
        self.draw_pokemons()
        match self.menu_state:
            case "battle_stage":
                self.draw_menu_options()
            case "quit":
                self.draw_menu_options()
            case "display_team" | "select_pokemon_confirm":
                self.draw_menu_options()
