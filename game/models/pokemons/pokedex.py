import json

from game.models.pokemons.pokemons import Pokemon
from game._all_paths_ import POKEMON_DICT_PATH, TYPES_CHART_PATH, BATTLE_BIOMES_PATH

class Pokedex:
    pokemon_dict = {}
    types_chart = {}
    def __init__(self, player_data):
        self.__dict__.update(**player_data)
        self.init_player_team()
        self.get_average_level()
        self.save = False

    def init_pokedex_data():
        with open(POKEMON_DICT_PATH, "r") as file:
            Pokedex.pokemon_dict = json.load(file)
            Pokemon.pokemon_dict = Pokedex.pokemon_dict
        with open(TYPES_CHART_PATH, "r") as file:
            Pokedex.types_chart = json.load(file)
        with open(BATTLE_BIOMES_PATH,"r") as file:
            Pokedex.battle_biomes = json.load(file)
    
    def compress_data(self, chosen_save : str) -> dict:
        player_data : dict = {
            "player" : self.player,
            "save" : chosen_save,
            "encounters" : {
                "done" : self.encounters["done"],
                "won" : self.encounters["won"],
                "lost" : self.encounters["lost"],
            },
            "active_team" : {}
        }
        for pokemon in self.player_team:
            index = str(self.player_team.index(pokemon) + 1)
            player_data["active_team"].update({
                "pokemon_" + index : {
                    "entry" : pokemon.entry,
                    "experience_points" : pokemon.experience_points
                    }
                }
            )
        return player_data
    
    def init_player_team(self):
        self.player_team = []
        for pokemon_data in list(self.active_team.keys()):
            pokemon = self.add_pokemon(self.active_team[pokemon_data]["entry"],\
                                       self.active_team[pokemon_data]["experience_points"])
            self.player_team.append(pokemon)
    
    def catch_pokemon(self, entry, experience_points=0):
        caught_pokemon = self.add_pokemon(entry, experience_points)
        self.player_team.append(caught_pokemon)

    def add_pokemon(self, entry, experience_points=0):
        pokemon = Pokemon(Pokedex.pokemon_dict[entry], experience_points)
        return pokemon

    def switch_pokemon(self, old_index, new_index):
        self.player_team.insert(new_index, self.player_team.pop(old_index))
    
    def get_average_level(self):
        self.average_level : int = 0
        for pokemon in self.player_team:
            self.average_level += pokemon.level
        self.average_level /= len(self.player_team)
    
    def init_player_pokedex_data(self):
        pass