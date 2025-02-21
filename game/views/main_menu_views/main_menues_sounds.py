import pygame as pg

from game.views.sounds import Sounds

class Main_menues_sounds(Sounds):
    def init_main_menues_sounds(self):
        Sounds.__init__(self)
        self.init_sounds()
        self.init_main_menues_musics()
    
    def init_main_menues_musics(self):
        self.main_menues_musics : dict = {
            "title_screen" : pg.mixer.Sound(self.MUSIC_PATH + "title_screen_sound_track.mp3"),
        }