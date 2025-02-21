import pygame as pg

from game.control.models_controller import Models_controller
from game.control.in_game_controllers.new_game_controller import New_game_controller
from game.views.in_game_views.new_game_display import New_game_display
from game.views.in_game_views.game_menues_sounds import Game_menues_sounds

from game.models.pokemons.pokedex import Pokedex

pg.font.init()

class New_game(
    Models_controller, New_game_controller,
    New_game_display, Game_menues_sounds):
    """
        Initializes the New_game class by calling the constructors of parent classes.
    """
    def __init__(self):
        Models_controller.__init__(self)
        self.init_config()
        Pokedex.init_pokedex_data()

    def startup(self):
        """
            iInitializes all menu-related data, including configuring the game,
            loading starter Pokémon, and setting the menu state.
        """
        self.pokemon_starters = [
            Pokedex.pokemon_dict["0001"],
            Pokedex.pokemon_dict["0004"],
            Pokedex.pokemon_dict["0007"]
            ]
        self.init_new_game_display()
        self.init_game_menu_sounds()
        self.music_channel.play(self.launch_menu_musics_dict["new_game"])
        self.menu_state : str = "player_input"

    def update(self):
        """
            trigger all changes such as changing selected option
        """
        self.draw()

    def cleanup(self):
        """
            cleans up all menu related data
        """
        self.music_channel.stop()

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