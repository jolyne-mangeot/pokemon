import random
import secrets

class Battle:
    """
        Represents a Pokémon battle between player's team and enemy team.
    """
    def __init__(self, player_pokedex, enemy_team, types_chart, pokemon_dict, battle_biome, wild):
        """
            Initializes a Battle instance.
        """
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
        """
            Sets the active Pokémon for battle.
        """
        if player:
            self.active_pokemon = self.player_team[index]
        else:
            self.enemy_pokemon = self.enemy_team[index]
    
    def heal_all(self):
        for pokemon in self.player_team:
            pokemon.current_health_points = pokemon.health_points

    def attack(self, player=True, type_attack="normal"):
        """
            Performs an attack on the opponent's Pokémon.
        """
        if player:
            attacker = self.active_pokemon
            attacked = self.enemy_pokemon
        else:
            attacker = self.enemy_pokemon
            attacked = self.active_pokemon
        if random.randint(0,100) > 93 + attacker.level*0.05:
            return -1
        else:
            type_multiplicator = 1
            for type in attacked.type:
                type_multiplicator *= self.type_chart[type_attack][type]
            damage = ((attacker.level*128/5+2) * attacker.attack\
                    /(attacked.defense if (self.enemy_guarded if player else self.player_guarded) == False else attacked.defense*1.6))/50+2 * type_multiplicator
            attacked.current_health_points -= int(damage)
            if attacked.current_health_points < 0:
                attacked.current_health_points = 0
            self.player_guarded = False
            self.enemy_guarded = False
            return type_multiplicator

    def guard(self, player=True):
        """
            Sets the guard status, reducing damage from the next attack.
        """
        if player:
            self.player_guarded = True
        else:
            self.enemy_guarded = True

    def heal(self, player=True):
        if player:
            self.active_pokemon.current_health_points +=20
            if self.active_pokemon.current_health_points >\
                    self.active_pokemon.health_points:
                self.active_pokemon.current_health_points =\
                self.active_pokemon.health_points
        else:
            self.enemy_pokemon.current_health_points +=20
            if self.enemy_pokemon.current_health_points >\
                    self.enemy_pokemon.health_points:
                self.enemy_pokemon.current_health_points =\
                self.enemy_pokemon.health_points

    def catch_attempt(self):
        """
            Attempts to catch a wild Pokémon based on catch rate and health.
        """
        odds = (((3*self.enemy_pokemon.health_points) - (2*self.enemy_pokemon.current_health_points)) * \
                3*self.enemy_pokemon.catch_rate) / (3*self.enemy_pokemon.health_points)
        if secrets.randbelow(255) < odds:
            return True
        else:
            return False

    def check_victory_defeat(self, caught=False):
        if caught:
            return True
        if all(pokemon.current_health_points <= 0 for pokemon in self.enemy_team):
            self.check_lost_pokemons()
            return True
        if all(pokemon.current_health_points <= 0 for pokemon in self.player_team):
            self.check_lost_pokemons()
            return True
        return False
    
    def check_active_pokemon(self):
        """
            Checks the status of the active Pokémon and whether the enemy was defeated or caught.
        """
        if self.active_pokemon.current_health_points <= 0:
            return True
        if self.enemy_pokemon.current_health_points <= 0:
            return True
        else:
            return False
    
    def gain_experience_all(self, put_out_pokemons, not_put_out_pokemons):
        """
            Grants experience to all participating and non-participating Pokémon
        """
        for pokemon in put_out_pokemons:
            gained_experience = pokemon.gain_experience(self.enemy_pokemon)
        for pokemon in not_put_out_pokemons:
            pokemon.gain_experience(self.enemy_pokemon, True)
        return gained_experience

    def level_up_all(self):
        for pokemon in self.player_team:
            pokemon.level_up()

    def check_lost_pokemons(self):
        """
            Removes fainted Pokémon from the player's team.
        """
        for pokemon in self.player_team:
            if pokemon.current_health_points <= 0:
                index = self.player_team.index(pokemon)
                self.player_team.pop(index)
    
    def check_evolutions(self):
        """
            Checks if any Pokémon in the player's team is ready to evolve
        """
        for pokemon in self.player_team:
            if pokemon.level >= pokemon.evolution_level:
                pokemon.evolve()
                self.check_evolutions()

    def run_away(self):
        """
            Attempts to run away from battle based on level difference.
        """
        self.run_away_attempts +=1
        run_odds = ((((self.active_pokemon.level*128)/self.enemy_pokemon.level)) / 256) * (100 + 10*self.run_away_attempts)
        if random.randint(0, 100) < run_odds:
            return True
        else:
            return False