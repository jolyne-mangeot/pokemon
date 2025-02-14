import pygame as pg

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
        self.load_graphics_main_menues()
    
    def draw_main_menu(self):
        self.screen.fill((100,0,0))
    
    def update_menu(self):
        """
            update_menu checks for all changes keyboard or mouse
            related
        """
        pass
    
    def pre_render_options(self):
        """
            Selects a font and pre-renders it regardless of hovered / selected
            option. all for display
        """
        font_selected = pg.font.SysFont("arial", 40)
        font_deselected = pg.font.SysFont("arial", 40)

        rendered_dialog = {"deselected":[], "selected":[]}
        for option in self.options:
            deselected_render = font_deselected.render(option, 1, self.deselected_color)
            deselected_rect = deselected_render.get_rect()
            selected_render = font_selected.render(option, 1, self.selected_color)
            selected_rect = selected_render.get_rect()
            rendered_dialog["deselected"].append((deselected_render, deselected_rect))
            rendered_dialog["selected"].append((selected_render, selected_rect))
        self.rendered = rendered_dialog
    
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