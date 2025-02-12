import pygame as pg
from control.control import Control

class States(Control):
    player_pokedex = None
    new_fight = None

    def __init__(self):
        Control.init_config(self)
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None

    def get_event_menu(self, event):
        """
            get all events for Main_menu states from the main_game_loop
            in Control. is done after individual get_event from active menu
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.confirm_keys and\
              self.selected_index == len(self.next_list) - 1:
                self.select_option()
            elif pg.key.name(event.key) in self.up_keys:
                self.change_selected_option(-1)
            elif pg.key.name(event.key) in self.down_keys:
                self.change_selected_option(1)
    
    def get_event_confirm(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.left_keys:
                self.change_selected_option(-1)
            elif pg.key.name(event.key) in self.right_keys:
                self.change_selected_option(1)

    def select_option(self):
        """
            change the active state with done attribute and change it
            to correct user input
        """
        if self.selected_index == len(self.next_list):
            self.quit = True
        else:
            self.next = self.next_list[self.selected_index]
            self.done = True
            self.selected_index = 0

    def draw_menu_options(self):
        """
            for all launch_menu states, enumerate buttons and places them before
            checking for selected index button to place it on the same position
        """
        for index, option in enumerate(self.rendered["deselected"]):
            option[1].center = (self.screen_rect.centerx, self.from_top + index*self.spacer)
            if index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])
    
    def draw_confirm_options(self):
        for index, option in enumerate(self.rendered["deselected"]):
            option[1].center = (self.screen_rect.centerx-50 + index*100, self.screen_rect.centery)
            if index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])