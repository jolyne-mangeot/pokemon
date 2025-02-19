import pygame as pg

from game.control.models_controller import Models_controller
from game.views.main_menu_views.main_menues_display import Main_menues_display
from game.control.main_game_controllers.main_menues_controller import Main_menues_controller

class Title_menu(
    Models_controller, Main_menues_controller, 
    Main_menues_display):
    
    def __init__(self):
        """
            inits values specific to the menu such as navigation and
            placement of options
        """
        Models_controller.__init__(self)
        Main_menues_controller.__init__(self)

    def startup(self):
        """
            initiates all menu-related data
        """
        self.init_config()
        self.init_main_menu_display()
        self.init_title_menu_object()

    def cleanup(self):
        """
            cleans up all menu related data
        """
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
            if pg.key.name(event.key) in self.confirm_keys and self.title_menu.selected_index == 2:
                self.quit = True
            elif pg.key.name(event.key) in self.confirm_keys:
                self.select_option(self.title_menu)
        self.title_menu.get_event_vertical(event)
    
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
        sicon = pg.image.load("game/assets/graphics/pokemon/0001/mini.png")
        icon = pg.transform.scale (sicon, (250,250))
        self.draw_title_screen()
        self.title_menu.draw_vertical_options()
        self.screen.blit(icon, (0,0))