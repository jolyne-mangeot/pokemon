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

    def load_graphics_launch_menues(self):
        self.launch_menu_img=pg.image.load(GRAPHICS_PATH+"/media/"+"launch screen.png")
        self.launch_menu_img=pg.transform.scale(self.launch_menu_img, (self.screen_width,self.screen_height))

        self.pkmn_frame_img=pg.image.load(GRAPHICS_PATH+"/media/"+"pkmn frame.png")
        self.pkmn_frame_img=pg.transform.scale(self.pkmn_frame_img, (self.screen_width,self.screen_height))

        self.team_select_img=pg.image.load(GRAPHICS_PATH+"/media/"+"pkmn frame.png")
        self.team_select_img=pg.transform.scale(self.team_select_img, (self.screen_width,self.screen_height))
    
    def draw_launch_menu(self):
        self.launch_menu_img=pg.transform.scale(self.launch_menu_img, (self.screen_width,self.screen_height))
        self.screen.blit(self.launch_menu_img,(0,0))
    
    def draw_pkmn_frame(self):
        self.pkmn_frame_img=pg.transform.scale(self.pkmn_frame_img, (self.screen_width,self.screen_height))
        self.screen.blit(self.pkmn_frame_img,(0,0))
    
    def draw_team_select_img(self):
        self.team_select_img=pg.transform.scale(self.team_select_img, (self.screen_width,self.screen_height))
        self.screen.blit(self.team_select_img,(0,0))



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

