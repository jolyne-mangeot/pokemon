import json
from game.pokemons.pokemons import Pokemon
from game.__game_settings__ import POKEMON_DICT_PATH, SAVE_PATH

class Pokedex:
    def __init__(self):
        Pokedex.pokemon_dict = self.init_pokedex_data()
        self.player_team = []

    def init_pokedex_data(self):
        with open(POKEMON_DICT_PATH, "r") as file:
            pokemon_dict = json.load(file)
        return pokemon_dict
    
    def init_player_data(self, save):
        with open(SAVE_PATH + save + ".json", "r") as file:
            player_data = json.load(file)
        self.__dict__.update(**player_data)
        self.init_player_team()
    
    def init_player_team(self):
        for pokemon in list(self.active_team.keys()):
            self.add_pokemon(self.active_team[pokemon]["entry"], self.active_team[pokemon]["experience_points"])
            self.player_team.append(pokemon)

    def add_pokemon(self, entry, experience_points=0):
        pokemon = Pokemon(self.pokemon_dict[entry], experience_points)
    
    def check_evolutions(self):
        for pokemon in self.player_team:
            if pokemon.level >= pokemon.evolution_level:
                pokemon.evolve(Pokedex.pokemon_dict[pokemon.evolution])
    
    def init_player_pokedex_data(self):
        pass