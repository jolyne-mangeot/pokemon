import random
import secrets

class Battle:
    def __init__(self, player_pokedex, enemy_team, types_chart, pokemon_dict, battle_biome, wild):
        self.wild = wild
        self.battle_biome = battle_biome
        self.player_pokedex = player_pokedex
        self.player_team = player_pokedex.player_team
        self.enemy_team = enemy_team.player_team
        self.type_chart = types_chart
        self.pokemon_dict = pokemon_dict
        self.player_guarded = False
        self.enemy_guarded = False
        self.run_away_attempts = 0
    
    def spawn_pokemon(self, index, player=True):
        if player:
            self.active_pokemon = self.player_team[index]
        else:
            self.enemy_pokemon = self.enemy_team[index]
    
    def heal_all(self):
        for pokemon in self.player_team:
            pokemon.current_health_points = pokemon.health_points

    def attack(self, player=True):
        if player:
            attacker = self.active_pokemon
            attacked = self.enemy_pokemon
        else:
            attacker = self.enemy_pokemon
            attacked = self.active_pokemon
        type_multiplicator = 1
        for type in attacked.type:
            type_multiplicator *= self.type_chart[attacker.type[0]][type]
        damage = ((attacker.level*128/5+2) * attacker.attack\
                  /(attacked.defense if (self.enemy_guarded if player else self.player_guarded) == False else attacked.defense*2))/50+2 * type_multiplicator
        attacked.current_health_points -= int(damage)
        if attacked.current_health_points < 0:
            attacked.current_health_points = 0
        self.player_guarded = False
        self.enemy_guarded = False
        return type_multiplicator

    def guard(self, player=True):
        if player:
            self.player_guarded = True
        else:
            self.enemy_guarded = True

    def heal(self):
        pass

    def catch_attempt(self):
        odds = (((3*self.enemy_pokemon.health_points) - (2*self.enemy_pokemon.current_health_points)) * \
                3*self.enemy_pokemon.catch_rate) / (3*self.enemy_pokemon.health_points)
        if secrets.randbelow(255) < odds:
            return True
        else:
            return False

    def check_victory_defeat(self, caught, ran_away):
        if all(pokemon.current_health_points <=0 for pokemon in self.player_team):
            self.check_lost_pokemons()
            return "defeat"
    def check_victory_defeat(self, caught, ran_away):
        if all(pokemon.current_health_points <= 0 for pokemon in self.enemy_team):
            self.check_lost_pokemons()
            return "victory"
        if caught:
            self.check_lost_pokemons()
            return "enemy_caught"
        if ran_away:
            self.check_lost_pokemons()
            return "ran_away"
            return "caught"
        if ran_away:
            return "ran_away"
    
    def check_active_pokemon(self, put_out_pokemons, not_put_out_pokemons, caught):
        if self.active_pokemon.current_health_points <= 0:
            return "active_beat"
        elif self.enemy_pokemon.current_health_points <= 0:
            self.gain_experience_all(put_out_pokemons, not_put_out_pokemons)
            return "enemy_beat"
        elif caught:
            self.gain_experience_all(put_out_pokemons, not_put_out_pokemons)
            return "enemy_caught"
        else:
            return None
    
    def gain_experience_all(self, put_out_pokemons, not_put_out_pokemons):
        for pokemon in put_out_pokemons:
            pokemon.gain_experience(self.enemy_pokemon)
            pokemon.level_up()
        for pokemon in not_put_out_pokemons:
            pokemon.gain_experience(self.enemy_pokemon, True)
            pokemon.level_up()

    def check_lost_pokemons(self):
        for pokemon in self.player_team:
            if pokemon.current_health_points <= 0:
                index = self.player_team.index(pokemon)
                self.player_team.pop(index)
    
    def check_evolutions(self):
        for pokemon in self.player_team:
            if pokemon.level >= pokemon.evolution_level:
                pokemon.evolve()
                self.check_evolutions()

    def run_away(self):
        self.run_away_attempts +=1
        run_odds = ((((self.active_pokemon.level*128)/self.enemy_pokemon.level)) / 256) * (100 + 10*self.run_away_attempts)
        if random.randint(0, 100) < run_odds:
            return True
        else:
            return False