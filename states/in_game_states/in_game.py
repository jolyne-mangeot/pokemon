import pygame as pg
from control.states_control import States

pg.font.init()

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = "main_menu"

    def cleanup(self):
        # cleans up all menu related data
        pass

    def startup(self):
        # initiates all menu related data
        pass

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN:
            self.done = True
        
    def update(self):
        self.draw()
    
    def draw(self):
        self.screen.fill((0,0,255))
