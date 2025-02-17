import pygame as pg

from game.views.display import Display

class Option_menu_class(Display):
    def __init__(self, margins, options, next_list=None):
        Display.__init__(self)
        self.from_left, self.from_top, self.spacer = margins
        self.options = options
        self.next_list = next_list
        self.selected_index = 0
        self.picked_index = None
        self.selected_color = (255,255,0)
        self.deselected_color = (255,255,255)
        self.picked_color = (255,0,0)
        self.pre_render()
    
    def update_colors(self, deselected_color, selected_color=None, picked_color=None):
        self.deselected_color = deselected_color
        
        if selected_color != None:
            self.selected_color = selected_color
        else:
            self.selected_color = deselected_color

        if picked_color != None:
            self.picked_color = picked_color
        else:
            self.picked_color = deselected_color
        self.pre_render()

    def update_options(self, options, next_list = None):
        self.options = options
        self.next_list = next_list
        self.pre_render()

    def pre_render(self):
        rendered_dialog = {"picked" : [], "deselected":[], "selected":[]}

        for option in self.options:
            picked_render = self.pixel_font_menu_selected.render(option, True, self.picked_color)
            picked_rect = picked_render.get_rect()
            deselected_render = self.pixel_font_menu_deselected.render(option, True, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            selected_render = self.pixel_font_menu_selected.render(option, True, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_dialog["picked"].append((picked_render, picked_rect))
            rendered_dialog["deselected"].append((deselected_render, deselected_rect))
            rendered_dialog["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_dialog
        self.rendered_team = rendered_dialog

    def draw_vertical_options(self):
        """
            for all launch_menu states, enumerate buttons and places them before
            checking for selected index button to place it on the same position
        """
        for index, option in enumerate(self.rendered["deselected"]):
            option[1].center = (self.from_left, self.from_top + index*self.spacer)
            if index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])
    
    def draw_horizontal_options(self):
        for index, option in enumerate(self.rendered["deselected"]):
            if len(self.rendered["deselected"]) == 2:
                option[1].center = (self.screen_rect.centerx-50 + index*100, self.from_top)
            else:
                option[1].center = (self.screen_rect.centerx-200 + index*200, self.from_top)
            if index == self.selected_index:
                if bool(self.picked_index):
                    if self.selected_index == self.picked_index:
                        continue
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])
    
    def draw_picked_options(self):
        for index, option in enumerate(self.rendered["deselected"]):
            option[1].center = (self.from_left, self.from_top + index*self.spacer)
            if index == self.picked_index:
                selected_render = self.rendered["picked"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            elif index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])

    def draw_chart_options(self):
        for index, option in enumerate(self.rendered["deselected"]):
            if index%2 == 0:
                option[1].center = (
                    self.from_left,
                    self.from_top + self.spacer*index/2
                )
            elif index == 6:
                option[1].center = (
                    self.from_left + (self.from_left*1.25),
                    self.from_top + self.spacer*index/2
                )
            else:
                option[1].center = (
                    self.from_left + (self.from_left*1.5),
                    self.from_top + self.spacer*(index-1)/2
                )
            if index == self.selected_index:
                selected_render = self.rendered_team["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])

    def get_event_vertical(self, event):
        """
            get all events for Main_menu states from the main_game_loop
            in Control. is done after individual get_event from active menu
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.up_keys:
                self.change_selected_option(-1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(-1)
            elif pg.key.name(event.key) in self.down_keys:
                self.change_selected_option(1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(1)
    
    def get_event_horizontal(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.left_keys:
                self.change_selected_option(-1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(-1)
            elif pg.key.name(event.key) in self.right_keys:
                self.change_selected_option(1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(1)

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

    # def select_option(self):
    #     """
    #         change the active state with done attribute and change it
    #         to correct user input
    #     """
    #     if self.selected_index == len(self.next_list):
    #         self.quit = True
    #     else:
    #         self.next = self.next_list[self.selected_index]
    #         self.done = True
    #         self.selected_index = 0