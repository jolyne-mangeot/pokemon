import json
from game.pokemons.pokemons import Pokemon
from game.__game_settings__ import POKEMON_DICT_PATH

class Pokedex:
    def __init__(self, wild=False, **player_data):
        self.__dict__.update(**player_data)
        self.wild = wild
        self.init_player_team()
        self.get_average_level()

    def init_pokedex_data(self):
        with open(POKEMON_DICT_PATH, "r") as file:
            Pokedex.pokemon_dict : dict = json.load(file)
    
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

    def add_pokemon(self, entry, experience_points=0):
        pokemon = Pokemon(Pokedex.pokemon_dict[entry], experience_points, self.wild)
        return pokemon

    def switch_pokemon(self, old_index, new_index):
        self.player_team.insert(new_index, self.player_team.pop(old_index))
    
    def check_evolutions(self):
        for pokemon in self.player_team:
            if pokemon.level >= pokemon.evolution_level:
                new_entry = pokemon.evolution
                pokemon.evolve(Pokedex.pokemon_dict[new_entry])
                self.check_evolutions()
    
    def get_average_level(self):
        self.average_level_list : list = []
        for pokemon in self.player_team:
            self.average_level_list.append(pokemon.level)
        for levels in self.average_level_list:
            self.average_level += levels
        self.average_level /= len(self.player_team)
    
    def init_player_pokedex_data(self):
        pass