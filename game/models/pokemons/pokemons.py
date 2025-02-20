class Pokemon:

    pokemon_dict = {}
    """
        This is the Pokemon class, representing a Pokémon character with attributes such as
        level, stats, experience points, and evolution properties.
    """
    def __init__(self, pokedex_entry, experience_points):
        """
        Initializes a new instance of a Pokémon. Takes in a pokedex entry (dictionary)
        and the current experience points of the Pokémon.
        """
        self.evolution_level = 100000000
        self.evolution = str(int(pokedex_entry['entry'])+1)
        while len(self.evolution) < 4:
            self.evolution = "0" + str(self.evolution)
        self.__dict__.update(pokedex_entry)
        self.experience_points : int = experience_points
        self.get_level()
        self.get_stats()
        self.restore_max_health()
    
    def restore_max_health(self):
        self.current_health_points = self.health_points

    def get_level(self):
        """
        Determines the Pokémon's current level based on experience points.
        """
        for potential_level in range (1,101):
            level_experience = potential_level ** 3
            if level_experience > self.experience_points:
                self.level = potential_level-1
                self.current_experience = self.experience_points - (self.level**3)
                break

    def get_stats(self):
        """
        Calculates the Pokémon's attack, defense, and health points based on its base stats
        and current level using a standard Pokémon stat formula.
        """
        self.attack = round(((self.base_attack*2) * self.level)/100 + 5, 0)
        self.defense = round(((self.base_defence*2) * self.level)/100 + 5, 0)
        self.health_points = round(((self.base_health_points*2) * self.level)/100 + self.level+10, 0)
    
    def gain_experience(self, defeated_pokemon, reduced=False):
        """
        This method increases the Pokémon's experience when it defeats another Pokémon.
        """
        gained_experience = round(((defeated_pokemon.yield_experience*defeated_pokemon.level)/7 * 1.5) * (0.5 if reduced else 1),0)
        self.experience_points += gained_experience
        self.current_experience += gained_experience
        return gained_experience

    def evolve(self):
        """
        This method triggers the evolution of the Pokémon if it has reached the required
        evolution level.
        """
        if self.level >= self.evolution_level:
            self.__init__(Pokemon.pokemon_dict[self.evolution], self.experience_points)
    
    def level_up(self):
        """
        This method checks if the Pokémon has enough experience to level up. If it does,
        the level increases, experience consumption is calculated, and stats are updated.
        """
        if self.level == 1:
            consummed_experience = 8
        else:
            consummed_experience = ((self.level+1) ** 3) - (self.level ** 3)
        if self.current_experience > consummed_experience:
            self.level += 1
            self.current_experience = self.current_experience - consummed_experience
            self.get_stats()
            self.level_up()