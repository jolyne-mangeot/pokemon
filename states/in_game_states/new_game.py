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
        self.next = ""
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
        self.menu_state = "player_input"
        self.update_options()

    def init_render_option(self):
        self.options = []
        self.next_list = []
    
    def init_save_file(self):
        current_player = {"player" : self.player, # get with input
                          "active_team" : {
                              "pokemon_1" : {
                                  "entry" : self.chosenpokemon, # get with choice
                                  "experience_points" : 125
                              }
                          }}
        current_pokedex = Pokedex(current_player)
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
                back = "pokemon_choice"
                self.get_event_pokemon_choice(event)
                self.get_event_menu(event)
            case "player_input":
                back = "player_input"
                self.get_event_player_input(event)
            case "quit":
                self.get_event_quit(event, back)
                self.get_event_confirm(event)
            # case "main" | _:
            #     back = "main"
            #     self.get_event_main(event)
            #     self.get_event_menu(event)

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
            case "main":
                self.draw_menu_options()
            case "player_input":
                self.draw_player_input(self.dialogs["your name"])
            case "pokemon_choice" | "quit":
                self.draw_confirm_options()