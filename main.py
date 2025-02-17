import pygame as pg

from control.control import Control

from states.main_menu_states.title_menu import Title_menu
from states.main_menu_states.preferences_menu import Preferences_menu
from states.main_menu_states.load_menu import Load_menu
from states.in_game_states.new_game import New_game
from states.in_game_states.launch_menu import Launch_menu
from states.in_game_states.in_fight import In_fight

pg.init()
game = Control()
game.init_settings()
game.init_config()

STATE_DICT = {
    "title_menu" : Title_menu(),
    "options" : Preferences_menu(),
    "new_game" : New_game(),
    "load_menu" : Load_menu(),
    "in_fight" : In_fight(),
    "launch_menu" : Launch_menu()
}

game.setup_states(STATE_DICT, "title_menu")
game.main_game_loop()

pg.quit()
exit()