import json
from game.pokemons.pokemons import Pokemon
from game.__game_settings__ import POKEMON_DICT_PATH, SAVE_PATH

class Pokedex:
    def __init__(self):
        self.init_pokedex_data()
        self.player_team = []

    def init_pokedex_data(self):
        with open(POKEMON_DICT_PATH, "r") as file:
            Pokedex.pokemon_dict = json.load(file)
    
    # def init_player_data(self, save):
    #     with open(SAVE_PATH + save + ".json", "r") as file:
    #         player_data = json.load(file)
    #     self.__dict__.update(**player_data)
    #     self.init_player_team()
    
    def init_player_team(self):
        for pokemon_data in list(self.active_team.keys()):
            pokemon = self.add_pokemon(self.active_team[pokemon_data]["entry"],\
                                       self.active_team[pokemon_data]["experience_points"])
            self.player_team.append(pokemon)

    def add_pokemon(self, entry, experience_points=0):
        pokemon = Pokemon(self.pokemon_dict[entry], experience_points)
        return pokemon
    
    def check_evolutions(self):
        for pokemon in self.player_team:
            if pokemon.level >= pokemon.evolution_level:
                if bool(pokemon.evolution):
                    new_entry = pokemon.evolution
                else:
                    new_entry = int(pokemon.entry)+1
                    new_entry = "00" + str(new_entry)
                pokemon.evolve(Pokedex.pokemon_dict[new_entry])
    
    def init_player_pokedex_data(self):
        pass