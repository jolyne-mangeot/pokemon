import pygame as pg
from control.states_control import States

class Main_menu_manager:
    def __init__(self):
        """
            inits selected option, last option to check for on-same-button
            mouse-hover, and misc. values like font color. for all main_menu
            derived classes
        """
        self.selected_index = 0
        self.last_option = None
        self.selected_color = (255,255,0)
        self.deselected_color = (255,255,255)
    
    def draw_menu_options(self):
        """
            for all main_menu states, enumerate buttons and places them before
            checking for selected index button to place it on the same position
        """
        self.screen.fill((100,0,0))
        for index, option in enumerate(self.rendered["deselected"]):
            option[1].center = (self.screen_rect.centerx, self.from_top + index*self.spacer)
            if index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])
    
    def update_menu(self):
        """
            update_menu checks for all changes keyboard or mouse
            related
        """
        pass
    
    def get_event_menu(self, event):
        """
            get all events for Main_menu states from the main_game_loop
            in Control. is done after individual get_event from active menu
        """
        if event.type == pg.KEYDOWN:
            if event.key in [pg.K_RETURN] and\
              self.selected_index == len(self.next_list) - 1:
                self.select_option()
    
    def pre_render_options(self):
        """
            Selects a font and pre-renders it regardless of hovered / selected
            option. all for display
        """
        font_selected = pg.font.SysFont("arial", 40)
        font_deselected = pg.font.SysFont("arial", 40)

        rendered_msg = {"deselected":[], "selected":[]}
        for option in self.options:
            deselected_render = font_deselected.render(option, 1, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            selected_render = font_selected.render(option, 1, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_msg["deselected"].append((deselected_render, deselected_rect))
            rendered_msg["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_msg
    
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
    
    def change_selected_option(self, operant):
        """
            for keyboard behaviour, change based on operant the selected
            option : single direction for now (up or down)
        """
        self.selected_index += operant
        max_indicator = len(self.rendered["deselected"]) - 1
        if self.selected_index < 0:
            self.selected_index = max_indicator
        elif self.selected_index > max_indicator:
            self.selected_index = 0