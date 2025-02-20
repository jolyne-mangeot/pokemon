import pygame as pg

from game.views.sounds import Sounds

class Main_menues_sounds(Sounds):
    def init_main_menu_sounds(self):
        Sounds.__init__(self)
        self.init_sounds()
        self.init_main_menues_musics()
        self.init_main_menu_sounds()
    
    def init_main_menues_sounds(self):
        self.main_menues_sounds = {

        }
    
    def init_main_menues_musics(self):
        self.main_menues_musics = {
            "title_screen" : pg.mixer.Sound(self.MUSIC_PATH + "title_screen_sound_track.mp3"),
            "launch_menu" : pg.mixer.Sound(self.MUSIC_PATH + "launch_menu_sound_track.mp3"),
            "launch_menu_night" : pg.mixer.Sound(self.MUSIC_PATH + "launch_menu_night_sound_track.mp3"),
        }