import pygame as pg
from datetime import datetime
import random

from game.control.models_controller import Models_controller
from game.control.in_game_controllers.launch_menu_controller import Launch_menu_controller
from game.views.in_game_views.launch_menu_display import Launch_menu_display
from game.views.in_game_views.game_menues_sounds import Game_menues_sounds

from game.models.pokemons.pokedex import Pokedex
from game.models.pokemons.battle import Battle

class Launch_menu(
    Models_controller, Launch_menu_controller,
    Launch_menu_display, Game_menues_sounds):
    """
        The Launch_menu class manages the game's launch menu.
        It handles menu initialization, updates, event handling, and launching battles.
    """
    
    def __init__(self):
        """
            Initializes the Launch_menu with default values.
        """
        Models_controller.__init__(self)
        self.back = "title_menu"
        self.focused_pokemon = None
        self.init_config()
        self.init_in_launch_config()
        self.init_game_menu_sounds()
    
    def init_in_launch_config(self):
        self.options_menu_event_dict = {
            "lost_game": self.get_event_lost_game,
            "launch_battle_confirm": self.get_event_launch_battle_confirm,
            "manage_team": self.get_event_manage_team,
            "pokedex_menu" : self.get_event_pokedex_menu,
            "save": self.get_event_save,
            "save_confirm": self.get_event_save_confirm,
            "quit": self.get_event_quit,
            "delete_save": self.get_event_delete_save,
            "main_launch_menu": self.get_event_main_launch_menu
        }
        self.options_menu_draw_dict = {
            "lost_game": self.draw_launch_menu_lost_game,
            "main_launch_menu": self.draw_main_launch_menu,
            "save": self.draw_save_menu,
            "manage_team": self.draw_manage_team_menu,
            "pokedex_menu" : self.draw_pokedex_menu,
            "save_confirm": self.draw_save_confirm_menu,
            "quit": self.draw_quit_confirm_menu,
            "delete_save": self.draw_delete_save_confirm_menu,
            "launch_battle_confirm": self.draw_launch_battle_confirm_menu,
        }

    def startup(self):
        """
           Initializes all menu-related configurations and settings.
        """
        self.init_launch_menu_display()
        self.check_game_status()
        self.update_options("main_launch_menu")
        now_time = datetime.now()
        if 9 > int(now_time.strftime("%H")) > 17:
            self.music_channel.play(self.launch_menu_musics_dict["launch_menu"], -1)
        else:
            self.music_channel.play(self.launch_menu_musics_dict["launch_menu_night"], -1)
        self.pressed_keys = None
        self.focused_found = False

    def update(self):
        """
            trigger all changes such as changing selected option
        """
        self.pressed_keys = pg.key.get_pressed()
        self.draw()

    def cleanup(self):
        """
            cleans up all menu related data
        """
        self.focused_found = False
        pass
    
    def launch_battle(self):
        """
        Starts a new battle by selecting an enemy Pokémon based on the player's Pokedex.
        """
        battle_level = (int(self.player_pokedex.average_level*0.9) ** 3, 
                        int(self.player_pokedex.average_level*1.1) ** 3)
        wild = True
        battle_biome = self.player_pokedex.battle_biomes[
            list(self.player_pokedex.battle_biomes.keys())[self.launch_battle_menu.selected_index]
        ]
        enemy_entry = random.choice(battle_biome["spawnable pokemons"])
        if self.focused_pokemon != None:
            if random.randint(0,100) > 60:
                enemy_entry = self.focused_pokemon
                self.focused_found = True
                self.focused_pokemon = None
        encounter = {
            "pokedex" : [],
            "active_team": {
                "pokemon_1": {
                    "entry": enemy_entry,
                    "experience_points": random.randrange(
                        (battle_level[0] if battle_level[0] > 0 else 1),
                        (battle_level[1] if battle_level[1] <= 999999 else 999999))
                }
            }
        }
        enemy_team = Pokedex(encounter)
        if not self.focused_found:
            enemy_team.check_evolutions()
        Models_controller.new_battle = Battle(self.player_pokedex, enemy_team, Pokedex.types_chart, Pokedex.pokemon_dict, battle_biome, wild)