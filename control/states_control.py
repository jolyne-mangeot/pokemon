from control.control import Control

class States(Control):
    player_pokedex = {}
    def __init__(self):
        Control.init_config(self)
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None