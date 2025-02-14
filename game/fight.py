import random

class Fight:
    def __init__(self, player_pokedex, enemy_team, types_chart):
        self.player_pokedex = player_pokedex
        self.player_team = player_pokedex.player_team
        self.enemy_team = enemy_team.player_team
        self.type_chart = types_chart
    
    def spawn_pokemon(self, index, player=True):
        if player:
            self.active_pokemon = self.player_team[index]
        else:
            self.enemy_pokemon = self.enemy_team[index]

    def attack(self, player=True):
        if player:
            attacker = self.active_pokemon
            attacked = self.enemy_pokemon
        type_multiplicator = 1
        for type in attacked.type:
            type_multiplicator *= self.type_chart[attacker.type[0]][type]
        damage = ((attacker.level*128/5+2) * attacker.attack/attacked.defense)/50+2 * type_multiplicator
        attacked.current_health_points -= damage
        return type_multiplicator

    def guard(self):
        pass

    def heal(self):
        pass

    def capture(self):
        pass

    def run_away(self):
        if random.randint(0, 100) > ((((self.active_pokemon.level*128)/self.enemy_pokemon.level) + 200) / 256) * 100:
            return True
        else:
            return False