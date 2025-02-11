import json
from game.pokemons.pokemons import Pokemon
from game.__game_settings__ import POKEDEX_DICT_PATH, SAVE_PATH

class Pokedex(Pokemon):
    def __init__(self, save):
        player_data = self.init_player_data("save_1")
        self.__dict__.update(**player_data)
        for pokemon in list(self.active_team.keys()):
            pass

    def init_pokedex_data(self):
        with open(POKEDEX_DICT_PATH, "r") as file:
            pokedex_reference = json.load(file)
        return pokedex_reference
    
    def init_player_data(self, save):
        with open(SAVE_PATH + save + ".json", "r") as file:
            player_data = json.load(file)
        return player_data
    
    def init_player_pokedex_data(self):
        pass