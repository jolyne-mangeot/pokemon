import json
from game.pokemons.pokemons import Pokemon
from game.__game_settings__ import POKEMON_DICT_PATH, SAVE_PATH

class Pokedex:
    def __init__(self, save):
        player_data = self.init_player_data("save_1")
        self.pokemon_list = self.init_pokedex_data
        self.__dict__.update(**player_data)
        for pokemon in list(self.active_team.keys()):
            pass

    def init_pokedex_data(self):
        with open(POKEMON_DICT_PATH, "r") as file:
            pokemon_list = json.load(file)
        return pokemon_list
    
    def init_player_data(self, save):
        with open(SAVE_PATH + save + ".json", "r") as file:
            player_data = json.load(file)
        return player_data

    def add_pokemon(self, index=0, experience_points=0):
        pokemon = Pokemon(self.pokemon_list[index], experience_points)
    
    def init_player_pokedex_data(self):
        pass