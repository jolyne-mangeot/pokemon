import pygame as pg
import random

from control.states_control import States
from views.in_game_views.launch_menu_display import Launch_menu_display
from states.in_game_states._game_menu_manager_ import Game_menu_manager
from states.in_game_states._launch_menu_states_ import Launch_menu_states

from game.pokemons.pokedex import Pokedex
from game.fight import Fight

class Launch_menu(States, Game_menu_manager, Launch_menu_display, Launch_menu_states):
    def __init__(self):
        States.__init__(self)
        Game_menu_manager.__init__(self)
        self.next = ""
        self.back = "main_menu"

    def cleanup(self):
        """
            cleans up all menu related data
        """
        self.picked_index = None
        self.rendered_picked = {}

    def startup(self):
        """
            initiates all menu-related data
        """
        self.init_config()
        self.init_launch_menu_display()
        self.picked_index = None
        self.rendered_picked = {}
        self.menu_state = "main_launch_menu"
        self.update_options()
    
    def launch_fight(self):
        # if self.player_pokedex.encounters['done'] % 5 == 0:
        #     wild = False
        #     pass #combat dresseur
        # else:
        fight_level = ((self.player_pokedex.average_level*0.9) ** 3, 
                        (self.player_pokedex.average_level*1.1) ** 3)
        wild = True
        encounter = {
            "active_team": {
                "pokemon_1": {
                    "entry": random.choice(list(self.player_pokedex.pokemon_dict.keys())),
                    "experience_points": random.randrange(int(fight_level[0]), int(fight_level[1]))
                }
            }
        }
        enemy_team = Pokedex(encounter)
        States.new_fight = Fight(self.player_pokedex, enemy_team, Pokedex.types_chart, Pokedex.pokemon_dict, wild)

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True

        match self.menu_state:
            case "launch_fight_confirm":
                if self.get_event_launch_fight_confirm(event):
                    self.next = "in_fight"
                    self.done = True
                    self.launch_fight()
            case "manage_team":
                self.get_event_manage_team(event)
            case "save":
                self.get_event_save(event)
            case "save_confirm":
                if self.get_event_save_confirm(event):
                    player_data = States.player_pokedex.compress_data(str(self.save_menu.selected_index + 1))
                    self.save_player_data(player_data, str(self.save_menu.selected_index + 1))
            case "quit":
                self.back = "main_launch_menu"
                self.get_event_quit(event)
            case "delete_save":
                if self.get_event_delete_save(event):
                    self.reset_player_data(States.player_pokedex.save)
            case "main_launch_menu" | _:
                self.get_event_main_launch_menu(event)
    
    def update(self):
        """
            trigger all changes such as changing selected option
        """
        self.update_menu()
        self.draw()
    
    def draw(self):
        """
            init all display related script
        """
        self.screen.fill((0,100,0))
        match self.menu_state:
            case "main_launch_menu":
                self.main_launch_menu.draw_vertical_options()
            case "save":
                self.save_menu.draw_vertical_options()
            case "manage_team":
                self.manage_team_menu.draw_picked_options()
            case "save_confirm" | "quit" | "delete_save" | "launch_fight_confirm":
                self.confirm_action_menu.draw_vertical_options()