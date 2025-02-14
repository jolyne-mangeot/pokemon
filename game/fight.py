import random

class Fight:
    def __init__(self, player_pokedex, enemy_team):
        self.player_pokedex = player_pokedex
        self.player_team = player_pokedex.player_team
        self.enemy_team = enemy_team.player_team
    
    def spawn_pokemon(self, index, player=True):
        if player:
            self.active_pokemon = self.player_team[index]
        else:
            self.enemy_pokemon = self.enemy_team[index]

    def attack(self, player=True):
        if player:
            attacker = self.active_pokemon
            attacked = self.enemy_pokemon
        if player:
            type_multiplicator = "a"
            damage = ((self.attacker.level*128/5+2) * self.attacker.attack/self.attacked.defence)/50+2 * type_multiplicator
            self.enemy_pokemon_current_health_points -= damage

    def guard(self):
        pass

    def heal(self):
        pass

    def capture(self):
        pass

    def run_away(self):
        if random.randint(0, 100) > ((((self.active_pokemon.level*128)/self.enemy_pokemon.level) + 50) / 256) * 100:
            return True
        else:
            return False