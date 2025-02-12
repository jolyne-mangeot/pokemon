import pygame as pg
from control.states_control import States
from states.main_menu_states.__main_menu_manager__ import Main_menu_manager
from states.in_game_states.pause_menu_save_quit import Pause_menu_save_quit

pg.font.init()

class Pause_menu(States, Main_menu_manager, Pause_menu_save_quit):
    def __init__(self):
        States.__init__(self)
        Main_menu_manager.__init__(self)
        self.next = ""
        self.back = "main_menu"
        self.from_top = self.screen_rect.height / 4
        self.spacer = 75
    
    def init_render_option_main(self):
        self.menu_state = "main"
        self.options = ["launch", "manage team", "manage met pokemons", "save", "quit"]
        self.next_list = ["in_fight", "manage_settings", "manage_settings", "save", "quit"]
    
    # def init_render_option_manage_team(self):
    #     self.menu_state = "manage_team"
    #     self.options = ["pokemon1", "pokemon2", self.dialogs["back"]]
    #     self.next_list = ["", "", "pause_menu"]

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
        self.init_render_option_main()
        self.pre_render_options()
        self.menu_state = "main"
        pass

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True

        match self.menu_state:
            case "save":
                self.chosen_save = self.get_event_save(event)
            case "save_confirm":
                if self.get_event_save_confirm(event) == True:
                    player_data = States.player_pokedex.compress_data()
                    self.save_player_data(player_data, self.chosen_save)
            case "quit":
                self.get_event_quit(event)
            case "main" | _:
                self.get_event_main(event)

        self.get_event_menu(event)
    
    def get_event_main(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_state = "quit"
                self.update_options()
            if pg.key.name(event.key) in self.confirm_keys and self.selected_index in (3,4):
                self.menu_state = self.next_list[self.selected_index]
                self.update_options()

    def update_options(self):
        match self.menu_state:
            case "save":
                self.init_render_option_save()
            case "save_confirm":
                self.init_render_option_save_confirm()
            case "quit":
                self.init_render_option_quit()
            case "main" | _:
                self.init_render_option_main()
        self.selected_index = 0
        self.pre_render_options()
    
    def update(self):
        """
            trigger all changes such as mouse hover or changing selected
            option, done after having checked in control class change on
            done and quit attribute from menu_manager inheritance
        """
        self.update_menu()
        self.draw()
    
    def draw(self):
        """
            init all display related script
        """
        self.draw_menu_options()
