import pygame as pg

from game.views.sounds import Sounds

class Game_menues_sounds(Sounds):
    def init_in_game_sounds(self):
        Sounds.__init__(self)
        self.init_sounds()
    
    def init_main_menues_sounds(self):
        self.main_menues_sounds = {

        }
    
    def init_main_menues_musics(self):
        self.main_menues_musics = {
            
        }