import pygame as pg

from game.views.display import Display
from game.views.sounds import Sounds

class Option_menu_model(Display, Sounds):
    """
        A class that represents an options menu model, inheriting from Display.   
    """
    def __init__(self, 
            margins, options, next_list=None, 
            deselected_color=(0,0,0), selected_color=(0,0,0), 
            picked_color=(255,0,0), images=False):
        """
         Initializes the menu with margins, a list of options, and optionally a next list.  
        """
        Display.__init__(self)
        Sounds.__init__(self)
        self.from_left, self.from_top, self.spacer = margins
        self.options = options
        self.next_list = next_list
        self.selected_index = 0
        self.picked_index = None
        self.selected_color = selected_color
        self.deselected_color = deselected_color
        self.picked_color = picked_color
        self.images = images
        self.pre_render()

    def pre_render(self):
        """
            Pre-renders the options in three states: picked, deselected, and selected.
        """
        rendered_dialog = {"picked" : [], "deselected":[], "selected":[]}

        for option in self.options:
            picked_render = self.pixel_font_menu_selected.render(option, True, self.picked_color)
            picked_rect = picked_render.get_rect()
            deselected_render = self.pixel_font_menu_deselected.render(option, True, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            self.pixel_font_menu_selected.set_bold(True)
            selected_render = self.pixel_font_menu_selected.render(option, True, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_dialog["picked"].append((picked_render, picked_rect))
            rendered_dialog["deselected"].append((deselected_render, deselected_rect))
            rendered_dialog["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_dialog

    def update_colors(self, deselected_color, selected_color=None, picked_color=None):
        """
            Updates the colors for deselected, selected, and picked options.
        """
        
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
        """
            Updates the list of options and optionally the next list
        """
        
        self.options = options
        self.next_list = next_list
        self.pre_render()

    def draw_vertical_options(self):
        """
            for all launch_menu states, enumerate buttons and places them before
            checking for selected index button to place it on the same position
        """
        for index, option in enumerate(self.rendered["deselected"]):
            option[1].center = (self.from_left, self.from_top + index*self.spacer)
            if index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].midbottom = option[1].midbottom
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])

    def draw_list_options(self):
        """
            for all launch_menu states, enumerate buttons and places them before
            checking for selected index button to place it on the same position
        """
        for index, option in enumerate(self.rendered["deselected"]):
            if self.selected_index-3 < index < self.selected_index:
                option[1].midbottom = (
                    self.from_left, 
                    self.from_top - (self.selected_index-index)*self.spacer
                )
                self.screen.blit(option[0],option[1])
            elif index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                option[1].midbottom = selected_render[1].midbottom = (
                    self.from_left, 
                    self.from_top
                )
                self.screen.blit(selected_render[0], selected_render[1])
            elif self.selected_index < index < self.selected_index+3:
                option[1].midbottom = (
                    self.from_left,
                    self.from_top + (index-self.selected_index)*self.spacer
                )
                self.screen.blit(option[0],option[1])
            if bool(self.images) and\
                  self.selected_index-3 < index < self.selected_index+3 :
                self.screen.blit(
                    self.images[index],
                    (
                        self.from_left*0.49,
                        option[1].centery-self.height*0.17
                    )
                )
    
    def draw_horizontal_options(self):
        """
            Draws the menu options in a horizontal arrangement.
            The selected option is highlighted based on its index.
        """
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
                selected_render[1].midbottom = option[1].midbottom
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])
    
    def draw_picked_options(self):
        """
            Draws the menu options with a picked option highlighted in red.
            Also highlights the currently selected option.
        """
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


    def draw_picked_list_options(self):
        """
            for all launch_menu states, enumerate buttons and places them before
            checking for selected index button to place it on the same position
        """
        for index, option in enumerate(self.rendered["deselected"]):
            if self.selected_index-3 < index < self.selected_index:
                if index == self.picked_index:
                    selected_render = self.rendered["picked"][index]
                    selected_render[1].midbottom = (
                        self.from_left, 
                        self.from_top - (self.selected_index-index)*self.spacer
                    )
                    self.screen.blit(selected_render[0],selected_render[1])
                else:
                    option[1].midbottom = (
                        self.from_left, 
                        self.from_top - (self.selected_index-index)*self.spacer
                    )
                    self.screen.blit(option[0],option[1])
            elif index == self.selected_index:
                if index == self.picked_index:
                    selected_render = self.rendered["picked"][index]
                    selected_render[1].midbottom = (
                        self.from_left, 
                        self.from_top
                    )
                    self.screen.blit(selected_render[0],selected_render[1])
                else:
                    selected_render = self.rendered["selected"][index]
                    option[1].midbottom = selected_render[1].midbottom = (
                        self.from_left, 
                        self.from_top
                    )
                    self.screen.blit(selected_render[0], selected_render[1])
            elif self.selected_index < index < self.selected_index+3:
                if index == self.picked_index:
                    selected_render = self.rendered["picked"][index]
                    selected_render[1].midbottom = (
                        self.from_left, 
                        self.from_top + (index-self.selected_index)*self.spacer
                    )
                    self.screen.blit(selected_render[0],selected_render[1])
                else:
                    option[1].midbottom = (
                        self.from_left,
                        self.from_top + (index-self.selected_index)*self.spacer
                    )
                    self.screen.blit(option[0],option[1])
            if bool(self.images) and\
                  self.selected_index-3 < index < self.selected_index+3 :
                self.screen.blit(
                    self.images[index],
                    (
                        self.from_left*0.49,
                        option[1].centery-self.height*0.17
                    )
                )

    def draw_chart_options(self):
        """
            Draws the menu options in a chart-like arrangement.
        """

        for index, option in enumerate(self.rendered["deselected"]):
            if index == len(self.rendered["deselected"]) - 1 and\
                    len(self.rendered["deselected"]) % 2 != 0:
                option[1].center = (
                    self.from_left*1.75,
                    self.from_top + self.spacer*index*0.56
                )
            elif index%2 == 0:
                option[1].center = (
                    self.from_left,
                    self.from_top + self.spacer*index*0.5
                )
            else:
                option[1].center = (
                    self.from_left*2.5,
                    self.from_top + self.spacer*(index-1)*0.5
                )
            if index == self.selected_index:
                selected_render = self.rendered["selected"][index]
                selected_render[1].center = option[1].center
                self.screen.blit(selected_render[0], selected_render[1])
            else:
                self.screen.blit(option[0],option[1])

    def get_event_vertical(self, event):
        """
            Processes vertical movement (up and down) in the menu based on key events.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.up_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
                self.change_selected_option(-1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(-1)
            elif pg.key.name(event.key) in self.down_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
                self.change_selected_option(1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(1)
    
    def get_event_horizontal(self, event):
        """
            Processes horizontal movement (left and right) in the menu based on key events.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.left_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
                self.change_selected_option(-1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(-1)
            elif pg.key.name(event.key) in self.right_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
                self.change_selected_option(1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(1)

    def get_event_chart(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.up_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
                self.change_selected_option(-2)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(-2)
            elif pg.key.name(event.key) in self.down_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
                self.change_selected_option(2)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(2)
            elif pg.key.name(event.key) in self.left_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
                self.change_selected_option(-1)
                while self.options[self.selected_index] == "":
                    self.change_selected_option(-1)
            elif pg.key.name(event.key) in self.right_keys:
                self.effects_channel.play(self.menues_sounds["cursor move"])
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