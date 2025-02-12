import pygame as pg
from control.states_control import States
from states.in_game_states.__game_menu_manager__ import Game_menu_manager
from states.in_game_states.launch_menu_states import Launch_menu_states

pg.font.init()

class Launch_menu(States, Game_menu_manager, Launch_menu_states):
    def __init__(self):
        States.__init__(self)
        Game_menu_manager.__init__(self)
        self.next = ""
        self.back = "main_menu"

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
        self.menu_state = "main"
        self.update_options()
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
                self.get_event_menu(event)
            case "save_confirm":
                if self.get_event_save_confirm(event) == True:
                    player_data = States.player_pokedex.compress_data()
                    self.save_player_data(player_data, self.chosen_save)
                self.get_event_confirm(event)
            case "quit":
                self.get_event_quit(event)
                self.get_event_confirm(event)
            case "main" | _:
                self.get_event_main(event)
                self.get_event_menu(event)

        

    def update_options(self):
        match self.menu_state:
            case "save":
                self.from_top = self.screen_rect.height / 3
                self.spacer = 60
                self.init_render_option_save()
            case "save_confirm":
                self.from_top = self.screen_rect.height/2 - 60
                self.spacer = 60
                self.init_render_option_confirm()
            case "quit":
                self.from_top = self.screen_rect.height/2 - 60
                self.spacer = 60
                self.init_render_option_confirm()
            case "main" | _:
                self.from_top = self.screen_rect.height / 4
                self.spacer = 60
                self.init_render_option_main()
        self.selected_index = 0
        self.pre_render_options()
    
    def update(self):
        """
            trigger all changes such as changing selected option
        """
        self.update_menu()
        self.draw()
    
    def draw(self):
        """
            init all display related script
        """
        self.screen.fill((0,100,0))
        match self.menu_state:
            case "main" | "save":
                self.draw_menu_options()
            case "save_confirm" | "quit":
                self.draw_confirm_options()
