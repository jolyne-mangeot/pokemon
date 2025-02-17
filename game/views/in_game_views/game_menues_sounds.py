import pygame as pg

from game.views.sounds import Sounds

class Game_menues_sounds(Sounds):
    def init_in_game_sounds(self):
        self.init_pokemons_cry()
        pass

    def init_pokemons_cry(self):
        for pokemon in self.player_pokedex.player_team:
            cry_path : str = self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/cry.ogg"
            pokemon.sound = pg.mixer.Sound(cry_path)
            pokemon.sound.set_volume(0.1*self.sfx_volume)
    
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
