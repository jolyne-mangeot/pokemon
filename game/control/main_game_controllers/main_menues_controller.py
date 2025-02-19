import pygame as pg

class Main_menues_controller:
    def __init__(self):
        """
            for all main_menu derived classes
        """
        pass

    def select_option(self, menu):
        """
            change the active state with done attribute and change it
            to correct user input
        """
        self.next = menu.next_list[menu.selected_index]
        self.done = True
    
    def update_menu(self):
        """
            update_menu checks for all changes keyboard or mouse
            related
        """
        pass