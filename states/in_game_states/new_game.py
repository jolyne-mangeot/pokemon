import pygame as pg
from control.states_control import States
from states.in_game_states.__game_menu_manager__ import Game_menu_manager
from states.in_game_states.__new_game_states__ import New_game_states
from game.pokemons.pokedex import Pokedex

pg.font.init()

class New_game(States, Game_menu_manager, New_game_states):
    def __init__(self):
        States.__init__(self)
        Game_menu_manager.__init__(self)
        self.next = "launch_menu"
        self.back = "main_menu"

    def cleanup(self):
        """
            cleans up all menu related data
        """
        pass

    def startup(self):
        """
            initiates all menu-related data
        """
        self.init_config()
        self.player_input : str = ""
        self.menu_state : str = "player_input"
        self.update_options()

    def init_render_option(self):
        self.options = []
        self.next_list = []
    
    def init_save_file(self):
        current_player : dict = {
                    "player" : self.player_input,
                    "encounters" : {
                        "done" : 0,
                        "won" : 0,
                        "lost" : 0
                    },
                    "active_team" : {
                        "pokemon_1" : {
                            "entry" : self.chosen_pokemon,
                            "experience_points" : 125
                        }
                    }}
        Pokedex.init_pokedex_data()
        current_pokedex = Pokedex(False, current_player)
        States.player_pokedex = current_pokedex

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True

        match self.menu_state:
            case "pokemon_choice":
                self.get_event_pokemon_choice(event)
                self.get_event_confirm(event)
            case "player_input":
                player_done = self.get_event_player_input(event)
                if player_done:
                    self.menu_state = "pokemon_choice"
                    self.update_options()
                elif player_done == False:
                    self.menu_state = "quit"
                    self.update_options()
            case "quit":
                self.get_event_quit(event)
                self.get_event_confirm(event)

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
            case "player_input":
                self.draw_player_input(self.dialogs["your name"])
            case "pokemon_choice" | "quit":
                self.draw_confirm_options()