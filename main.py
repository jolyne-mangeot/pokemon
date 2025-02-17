import pygame as pg

from control.control import Control

from states.main_menu_states.title_menu import Title_menu
from states.main_menu_states.preferences_menu import Preferences_menu
from states.main_menu_states.load_menu import Load_menu
from states.in_game_states.new_game import New_game
from states.in_game_states.launch_menu import Launch_menu
from states.in_game_states.in_fight import In_fight

# import tracemalloc, linecache
# def display_top(snapshot, key_type='lineno', limit=10):
#     snapshot = snapshot.filter_traces((
#         tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
#         tracemalloc.Filter(False, "<unknown>"),
#     ))
#     top_stats = snapshot.statistics(key_type)

#     print("Top %s lines" % limit)
#     for index, stat in enumerate(top_stats[:limit], 1):
#         frame = stat.traceback[0]
#         print("#%s: %s:%s: %.1f KiB"
#               % (index, frame.filename, frame.lineno, stat.size / 1024))
#         line = linecache.getline(frame.filename, frame.lineno).strip()
#         if line:
#             print('    %s' % line)

#     other = top_stats[limit:]
#     if other:
#         size = sum(stat.size for stat in other)
#         print("%s other: %.1f KiB" % (len(other), size / 1024))
#     total = sum(stat.size for stat in top_stats)
#     print("Total allocated size: %.1f KiB" % (total / 1024))
# tracemalloc.start()

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

# snapshot1 = tracemalloc.take_snapshot()
# STATE_DICT['load_menu'] = Load_menu()
# STATE_DICT['game'] = Game()

# STATE_DICT['pause_menu'] = Pause_menu()
# snapshot2 = tracemalloc.take_snapshot()

game.setup_states(STATE_DICT, "title_menu")
game.main_game_loop()

# snapshot3 = tracemalloc.take_snapshot()
# display_top(snapshot1)
# display_top(snapshot2)
# display_top(snapshot3)

pg.quit()
exit()