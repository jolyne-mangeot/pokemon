import pygame as pg

from game.control.control import Control

from game.models.main_menu_models.title_menu import Title_menu
from game.models.main_menu_models.preferences_menu import Preferences_menu
from game.models.main_menu_models.load_menu import Load_menu
from game.models.in_game_models.new_game import New_game
from game.models.in_game_models.launch_menu import Launch_menu
from game.models.in_game_models.in_battle import In_battle

pg.init()
game = Control()
game.init_settings()
game.init_config()

STATE_DICT = {
    "title_menu" : Title_menu(),
    "options" : Preferences_menu(),
    "new_game" : New_game(),
    "load_menu" : Load_menu(),
    "in_battle" : In_battle(),
    "launch_menu" : Launch_menu()
}

game.setup_states(STATE_DICT, "title_menu")
game.main_game_loop()

pg.quit()