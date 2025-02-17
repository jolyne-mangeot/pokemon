import pygame as pg

from control.states_control import States
from states.main_menu_states._main_menu_manager_ import Main_menu_manager

pg.font.init()

class Main_menu(States, Main_menu_manager):
    def __init__(self):
        """
            inits values specific to the menu such as navigation and
            placement of options
        """
        States.__init__(self)
        Main_menu_manager.__init__(self)
        self.next = ""
        self.next_list = ["load_menu", "options"]

        self.from_left = self.screen_rect.width/2
        self.from_top = 200
        self.spacer = 75
    
    def init_render_option(self):
        self.options = [self.dialogs['play'], self.dialogs['options'], self.dialogs['quit']]

    def cleanup(self):
        """
            cleans up all menu related data
        """
        pass

    def startup(self):
        """
            initiates all menu-related data
        """
        self.init_config()
        self.init_render_option()
        self.pre_render_options()
        pass

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys:
                self.quit = True
            elif pg.key.name(event.key) in self.confirm_keys:
                self.select_option()
        self.get_event_menu(event)
    
    def update(self):
        """
            trigger all changes such as changing selected option,
            done after having checked in control class change on
            done and quit attribute from menu_manager inheritance
        """
        self.update_menu()
        self.draw()
    
    def draw(self):
        """
            init all display related script
        """
        sicon = pg.image.load("assets/graphics/pokemon/0001/mini.png")
        icon = pg.transform.scale (sicon, (250,250))
        self.draw_main_menu()
        self.draw_menu_options()
        self.screen.blit(icon, (0,0))