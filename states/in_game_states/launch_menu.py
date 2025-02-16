import pygame as pg
import random
from control.states_control import States
from game.pokemons.pokedex import Pokedex
from game.fight import Fight
from states.in_game_states.__game_menu_manager__ import Game_menu_manager
from states.in_game_states.__launch_menu_states__ import Launch_menu_states

pg.font.init()

class Launch_menu(States, Game_menu_manager, Launch_menu_states):
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
        self.picked_index = None
        self.rendered_picked = {}
        self.menu_state = "main"
        self.update_options()
    
    def launch_fight(self):
        fight_level = (self.player_pokedex.average_level*0.9, self.player_pokedex.average_level*1.1)
        encounter = {
            "active_team": {
                "entry" : random.randint(self.player_pokedex.pokemon_dict.keys()),
                "experience_points" : random.randrange(fight_level**3)
            }
        }
        enemy_team = Pokedex(wild=True, **encounter)
        States.new_fight = Fight(self.player_pokedex.player_team, enemy_team)

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
                    self.launch_fight()
                self.get_event_confirm(event)
            case "manage_team":
                self.get_event_manage_team(event)
                self.get_event_menu(event)
            case "save":
                self.chosen_save = self.get_event_save(event)
                self.get_event_menu(event)
            case "save_confirm":
                if self.get_event_save_confirm(event):
                    player_data = States.player_pokedex.compress_data(self.chosen_save)
                    self.save_player_data(player_data, self.chosen_save)
                self.get_event_confirm(event)
            case "quit":
                self.back = "main"
                self.get_event_quit(event)
                self.get_event_confirm(event)
            case "delete_save":
                if self.get_event_delete_save(event):
                    self.reset_player_data(States.player_pokedex.save)
                self.get_event_confirm(event)
            case "main" | _:
                self.get_event_main(event)
                self.get_event_menu(event)
    
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
        #self.screen.fill((0,100,0))
        self.draw_launch_menu()
        match self.menu_state:
            case "main" | "save":
                self.draw_menu_options()
            case "manage_team":
                self.draw_menu_options()
                self.draw_picked()
            case "save_confirm" | "quit" | "delete_save":
                self.draw_confirm_options()
