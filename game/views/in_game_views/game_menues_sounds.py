import pygame as pg

from game.views.sounds import Sounds

class Game_menues_sounds(Sounds):
    def init_in_game_sounds(self):
        Sounds.__init__(self)
        self.init_sounds()
        self.init_pokemons_cry()
        pass

    def init_pokemons_cry(self):
        for pokemon in self.player_pokedex.player_team:
            cry_path : str = self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/cry.ogg"
            pokemon.sound = pg.mixer.Sound(cry_path)
            pokemon.sound.set_volume(0.1*self.sfx_volume)

    def init_in_battle_sounds(self):
        self.init_in_game_sounds()
        self.init_actions_sounds()
    
    def init_actions_sounds(self):
        self.level_up_sound = pg.mixer.Sound(self.SFX_PATH + "level_up.mp3")
        self.level_up2_sound = pg.mixer.Sound(self.SFX_PATH + "RBY_level_up.mp3")

        self.caught_pokemon_sound = pg.mixer.Sound(self.SFX_PATH + "caught-a-pokemon.mp3")
        self.recovery_sound = pg.mixer.Sound(self.SFX_PATH + "recovery.mp3")
        self.bump_wall_sound = pg.mixer.Sound(self.SFX_PATH + "bump_wall.mp3")
        self.battle_sound = pg.mixer.Sound(self.SFX_PATH + "batttle.mp3")
        self.item_found_sound = pg.mixer.Sound(self.SFX_PATH + "RBY_item-found.mp3")
        self.run_away_sound = pg.mixer.Sound(self.SFX_PATH + "run-away.mp3")
        self.pokemon_out_sound = pg.mixer.Sound(self.SFX_PATH + "pokemon-out.mp3")
        
        self.evolve_sound = pg.mixer.Sound(self.SFX_PATH + "evolve.mp3")
        self.evolving_theme_sound = pg.mixer.Sound(self.SFX_PATH + "evolving.mp3")
    

        self.Stat_Raise_Fell_sound = pg.mixer.Sound(self.SFX_PATH + "Stat_Raise_Fell.mp3")
        self.low_hp_pokemon_sound = pg.mixer.Sound(self.SFX_PATH + "low_hp_pokemon.mp3")
       
        self.hit_weak_not_very_effective_sound = pg.mixer.Sound(self.SFX_PATH + "hit_weak_not_very_effective.mp3")
        self.hit_super_effective_sound = pg.mixer.Sound(self.SFX_PATH + "hit_super_effective.mp3 ")



    def play_hit_weak_not_very_effective_sound(self):
        self.hit_weak_not_very_effective_sound.play()   
    
    def play_hit_super_effective_sound(self):
        self.hit_super_effective_sound.play()

    

    def play_caught_pokemon_sound(self):
        self.caught_pokemon_sound.play()

    def play_recovery_sound(self):
        self.recovery_sound.play()

    def play_bump_wall_sound(self):
        self.bump_wall_sound.play()
        
    def play_battle_sound(self):
        self.battle_sound.play()

    def play_item_found_sound(self):
        self.item_found_sound.play()

    def play_run_away_sound(self):
        self.run_away_sound.play()

    def play_pokemon_out_sound(self):
        self.pokemon_out_sound.play()

    def play_evolving_theme_sound(self):
        self.evolving_theme_sound.play() 

    def play_evolve_sound(self):
        self.evolve_sound.play()

        
  
    def play_Stat_Raise_Fell_sound(self):
        self.Stat_Raise_Fell_sound.play()

    def play_low_hp_pokemon_sound(self):
        self.low_hp_pokemon_sound.play()
    

    def play_active_pokemon_cry(self):
        self.battle.active_pokemon.sound.play()


    

    #     # self.sound_path = f"pokemon/assets/graphics/media/pokemon/{pokemon_entry}/cry.ogg"
        

    #     if os.path.exists(self.sound_path):
    #         self.sound = pg.mixer.Sound(self.sound_path)
    #         self.sound.set_volume(0.7)
    #     else:
    #         self.sound = None
    #         print(f"Sound file not Found: {self.sound_path}")
    # def play(self):
    #     if self.sound:
    #         self.sound.play()
    #     else:
    #         print("Error: Sound non loaded.")
