import json
from game.pokemons.pokemons import Pokemon
from game.__game_settings__ import POKEMON_DICT_PATH, SAVE_PATH

class Pokedex:
    def __init__(self, player_data):
        self.init_pokedex_data()
        self.__dict__.update(**player_data)
        self.init_player_team()

    def init_pokedex_data(self):
        with open(POKEMON_DICT_PATH, "r") as file:
            Pokedex.pokemon_dict = json.load(file)
    
    def compress_data(self):
        player_data = {
            "player" : self.player,
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
        pokemon = Pokemon(Pokedex.pokemon_dict[entry], experience_points)
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