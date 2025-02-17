import pygame as pg

class Main_menues_controller:
    def __init__(self):
        """
            inits selected option, last option to check for on-same-button
            mouse-hover, and misc. values like font color. for all main_menu
            derived classes
        """
        pass
    
    def update_menu(self):
        """
            update_menu checks for all changes keyboard or mouse
            related
        """
        pass

    def select_option(self, menu):
        """
            change the active state with done attribute and change it
            to correct user input
        """
        self.next = menu.next_list[menu.selected_index]
        self.done = True