import pygame as pg

from game.control.models_controller import Models_controller
from game.control.in_game_controllers.new_game_controller import New_game_controller
from game.views.in_game_views.new_game_display import New_game_display

from game.models.pokemons.pokedex import Pokedex

pg.font.init()

class New_game(
    Models_controller, New_game_controller,
    New_game_display):
    """
        Initializes the New_game class by calling the constructors of parent classes.
    """
    def __init__(self):
        Models_controller.__init__(self)

    def startup(self):
        """
            iInitializes all menu-related data, including configuring the game,
            loading starter Pokémon, and setting the menu state.
        """
        self.init_config()
        Pokedex.init_pokedex_data()
        self.pokemon_starters = [
            Pokedex.pokemon_dict["0001"],
            Pokedex.pokemon_dict["0004"],
            Pokedex.pokemon_dict["0007"]
            ]
        self.init_new_game_display()
        self.menu_state : str = "player_input"
        self.update_options()

    def cleanup(self):
        """
            cleans up all menu related data
        """
        pass

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
                self.pokemon_choice.get_event_horizontal(event)
            case "player_input":
                self.get_event_player_input(event)
                self.player_input.get_event_input(event)

    def update(self):
        """
            trigger all changes such as changing selected option
        """
        self.draw()
    
    def draw(self):
        """
            init all display related script
        """
        self.draw_action_background()
        match self.menu_state:
            case "player_input":
                self.draw_name_frame(self.width*0.188,self.height*0.475,self.width*0.62,self.height*0.07)
                self.player_input.draw_input()
            case "pokemon_choice":
                self.pokemon_choice.draw_horizontal_options()
                self.draw_starter_pokemon()

    def init_save_file(self):
        """
        Creates a save file containing the player's name, starter Pokémon, and initial stats.
        """
        self.chosen_pokemon = "000" + str(self.pokemon_choice.selected_index*3 + 1)
        current_player : dict = {
                    "player" : self.player_input.input,
                    "encounters" : {
                        "done" : 0,
                        "won" : 0,
                        "lost" : 0
                    },
                    "pokedex" : [
                        
                    ],
                    "active_team" : {
                        "pokemon_1" : {
                            "entry" : self.chosen_pokemon,
                            "experience_points" : 125
                        }
                    }}
        self.player_pokedex = Pokedex(current_player)
        Models_controller.player_pokedex = self.player_pokedex