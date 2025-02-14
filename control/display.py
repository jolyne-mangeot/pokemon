import pygame as pg
from control.__control_settings__ import GRAPHICS_PATH

class Display():
    def __init__(self):
        self.field=""
        self.screen_width=500
        self.screen_height=500
        self.screen=pg.display.set_mode((self.screen_width,self.screen_height))

    def load_battlefield(self):
        self.field_precombat=pg.image.load(GRAPHICS_PATH+"/media/"+"battlefield pre.png")
        self.field_combat=pg.image.load(GRAPHICS_PATH+"/media/"+"battlefield combat.png")
    
    def load_graphics_main_menues(self):
        self.titleimg=pg.image.load(GRAPHICS_PATH+"/media/"+"title screen.png")
        self.titleimg=pg.transform.scale(self.titleimg,(self.screen_width,self.screen_height))
        self.preferencesimg = pg.image.load(GRAPHICS_PATH+"/media/"+"preferences screen.png")
        self.preferencesimg=pg.transform.scale(self.preferencesimg,(self.screen_width,self.screen_height))
        self.loadimg=pg.image.load(GRAPHICS_PATH+"/media/"+"load screen.png")
        self.loadimg=pg.transform.scale(self.loadimg,(self.screen_width,self.screen_height))
    
    def load_screen(self):
        self.loadimg=pg.transform.scale(self.loadimg,(self.screen_width,self.screen_height))
        self.screen.blit(self.loadimg,(0,0))

    def title_screen(self):
        self.titleimg=pg.transform.scale(self.titleimg,(self.screen_width,self.screen_height))
        self.screen.blit(self.titleimg,(0,0))
    
    def preferences_screen(self):
        self.preferencesimg=pg.transform.scale(self.preferencesimg,(self.screen_width,self.screen_height))
        self.screen.blit(self.preferencesimg, (0,0))

    def draw_precombat_field(self):
        pg.transform.scale(self.field,(self.screen_width, self.screen_height))
        self.screen.blit(self.field,(0,0))
        
    def draw_combat_screen(self):
        pg.transform.scale(self.field,(self.screen_width, self.screen_height))
        self.screen.blit(self.field,(0,0))


########TODO remove later######TEST AREA#############
'''pg.init()

disp1=Display()

run=True

while run:
    events=pg.event.get()
    for event in events:
        if event.type==pg.QUIT:
            pg.quit()
            exit()
    disp1.title_screen()

    pg.display.flip()

pg.quit()'''

