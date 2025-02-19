import pygame as pg

from game.views.sounds import Sounds

class Game_menues_sounds(Sounds):
    """
    This class handles the initialization of various sounds in the game, including Pokémon cries and in-game sounds
    """
    def init_in_game_sounds(self):
        Sounds.__init__(self)
        self.init_sounds()
        self.init_pokemons_cry()

    def init_pokemons_cry(self):
        """
        Initialize Pokémon cry sounds based on the player's team
        """
        for pokemon in self.player_pokedex.player_team:
            cry_path : str = self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/cry.ogg"
            pokemon.sound = pg.mixer.Sound(cry_path)
            pokemon.sound.set_volume(0.1*self.sfx_volume)
    
    def init_enemy_pokemons_cry(self):
        for pokemon in self.battle.enemy_team:
            cry_path : str = self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/cry.ogg"
            pokemon.sound = pg.mixer.Sound(cry_path)
            pokemon.sound.set_volume(0.1*self.sfx_volume)
    
    def play_enemy_pokemon_cry(self):
        self.battle.enemy_pokemon.sound.play()

    def play_active_pokemon_cry(self):
        self.battle.active_pokemon.sound.play()

    def init_in_battle_sounds(self):
        """
        Initialize sound effects for in-game actions, such as leveling up
        """
        self.init_in_game_sounds()
        self.init_enemy_pokemons_cry()
        self.init_battle_actions_sounds()
        self.init_battle_music()
    
    def init_battle_music(self):
        self.in_battle_musics = {
            "caught pokemon" : pg.mixer.Sound(self.SFX_PATH + "caught-a-pokemon.mp3"),
            "battle music" : pg.mixer.Sound(self.SFX_PATH + "battle.mp3"),
        }
        for sound in list(self.in_battle_musics.keys()):
            self.in_battle_musics[sound].set_volume(0.1*self.music_volume)
    
    def init_battle_actions_sounds(self):
        self.in_game_actions_sounds = {
            "levelup" : pg.mixer.Sound(self.SFX_PATH + "level_up.mp3"),
            "RBY levelup" : pg.mixer.Sound(self.SFX_PATH + "RBY_level-up.mp3"),
            "health recovery" : pg.mixer.Sound(self.SFX_PATH + "recovery.mp3"),
            "RBY item found" : pg.mixer.Sound(self.SFX_PATH + "RBY_item-found.mp3"),
            "run away" : pg.mixer.Sound(self.SFX_PATH + "run-away.mp3"),
            "pokemon out" : pg.mixer.Sound(self.SFX_PATH + "pokemon-out.mp3"),
            "evolve" : pg.mixer.Sound(self.SFX_PATH + "evolve.mp3"),
            "evolving" : pg.mixer.Sound(self.SFX_PATH + "evolving.mp3"),
            # "stat raise" : pg.mixer.Sound(self.SFX_PATH + "Stat_Raise_Fell.mp3"),
            "low health" : pg.mixer.Sound(self.SFX_PATH + "low_hp_pokemon.mp3"),
            "hit no effective" : pg.mixer.Sound(self.SFX_PATH + "hit_no_effective.mp3"),
            "hit not very effective" : pg.mixer.Sound(self.SFX_PATH + "hit_weak_not_very_effective.mp3"),
            "hit very effective" : pg.mixer.Sound(self.SFX_PATH + "hit_super_effective.mp3 ")
        }
        for sound in list(self.in_game_actions_sounds.keys()):
            self.in_game_actions_sounds[sound].set_volume(0.1*self.sfx_volume)
        self.in_game_actions_sounds["pokemon out"].set_volume(0.03*self.sfx_volume)
