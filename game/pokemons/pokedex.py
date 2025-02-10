import json
from game.__game_settings__ import POKEDEX_DICT_PATH

class Pokedex:
    def __init__(self):
        pass

    def load_data(self):
        with open(POKEDEX_DICT_PATH, "r") as file:
            pokedex_reference = json.load(file)
        return pokedex_reference