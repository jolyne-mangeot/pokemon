import pygame as pg
from control.control import Control
from states.main_menu_states.main_menu import Main_menu
from states.main_menu_states.preferences_menu import Preferences_menu
from states.main_menu_states.load_menu import Load_menu
from states.in_game_states.in_game import Game
from states.in_game_states.pause_menu import Pause_menu

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
    'main_menu' : Main_menu(),
    'options' : Preferences_menu(),
    'load_menu' : Load_menu(),
    'game' : Game(),
    'pause_menu' : Pause_menu()
}

# snapshot1 = tracemalloc.take_snapshot()
# STATE_DICT['load_menu'] = Load_menu()
# STATE_DICT['game'] = Game()
# STATE_DICT['pause_menu'] = Pause_menu()
# snapshot2 = tracemalloc.take_snapshot()

game.setup_states(STATE_DICT, "main_menu")
game.main_game_loop()

# snapshot3 = tracemalloc.take_snapshot()
# display_top(snapshot1)
# display_top(snapshot2)
# display_top(snapshot3)

pg.quit()
exit()