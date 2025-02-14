class Pokemon:
    def __init__(self, pokedex_entry, experience_points, wild=False):
        self.evolution_level = 100000000
        self.evolution = str(int(pokedex_entry['entry'])+1)
        while len(self.evolution) < 4:
            self.evolution = "0" + str(self.evolution)
        self.__dict__.update(pokedex_entry)
        if wild:
            self.name = "Wild " + self.name
        self.experience_points : int = experience_points
        self.get_graphics()
        self.get_level()
        self.get_stats()
        self.restore_max_health()
    
    def restore_max_health(self):
        self.current_health_points = self.health_points
    
    def get_graphics(self):
        self.front_image = str(self.entry + "/front.png")
        self.back_image = str(self.entry + "/back.png")

    def get_level(self):
        for potential_level in range (1,101):
            level_experience = potential_level ** 3
            if level_experience > self.experience_points:
                self.level = potential_level-1
                self.current_experience = self.experience_points - (self.level**3)
                break

    def get_stats(self):
        self.attack = round(((self.base_attack*2) * self.level)/100 + 5, 0)
        self.defense = round(((self.base_defence*2) * self.level)/100 + 5, 0)
        self.health_points = round(((self.base_health_points*2) * self.level)/100 + self.level+10, 0)
    
    def gain_experience(self, defeated_pokemon):
        gained_experience = round((defeated_pokemon.yield_experience*defeated_pokemon.level)/7 * 1.5,0)
        self.experience_points += gained_experience
        self.current_experience += gained_experience
        self.level_up()

    def evolve(self):
        if self.level >= self.evolution_level:
            self.__init__(self.evolution, self.experience_points)
    
    def level_up(self):
        if self.level == 1:
            consummed_experience = 8
        else:
            consummed_experience = ((self.level+1) ** 3) - (self.level ** 3)
        if self.current_experience > consummed_experience:
            self.level += 1
            self.current_experience = self.current_experience - consummed_experience
            self.get_stats()
            self.level_up()

    # def print_stats(self):
    #     print(
    #         f"lvl : {self.level}",
    #         f"exp totale : {self.experience_points}",
    #         f"exp actuelle : {self.current_experience}",
    #         f"atk : {self.attack}, def : {self.defense}, pv : {self.health_points}",
    #         sep="\n")

# pokedex = {
#     "#0001" : {
#         "nom": "Bulbasaur",
#         "type": ["Grass", "Poison"],
#         "défense": 49,
#         "puissance_d_attaque": 49,
#         "point_de_vie": 45,
#         "evolution_level" : 16,
#         "evolution" : "#0002",
#         "yield_experience" : 64,
#         "images": {
#             "front": "img/001/front.png",
#             "back": "img/001/back.png"
#         }
#     }
# }
# gained_experience = round((pokedex["#0001"]['yield_experience']*54) / 7 * 1.5, 0)
# pokemon1 = Pokemon(pokedex["#0001"], 0)
# pokemon2 = Pokemon(pokedex["#0001"], 45000)
# pokemon1.gain_experience(pokemon2)
# pokemon1.print_stats()
# pokemon1.gain_experience(pokemon2)
# pokemon1.print_stats()
# pokemon1.gain_experience(pokemon2)
# pokemon1.print_stats()