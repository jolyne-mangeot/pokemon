import pygame as pg

class Launch_menu_controller:
    """
        This class manages the launch menu of the game. It updates menu options,
        handles user input, and manages game states.
    """
    def update_options(self, menu_state):
        """
        Updates the menu options based on the current menu state.
        """
        self.menu_state = menu_state
        match self.menu_state:
            case "manage_team":
                self.manage_team_menu.update_options(
                    self.init_render_option_team(self.player_pokedex.player_team, True),
                    images=self.load_manage_team_mini_images()
                )
                self.manage_team_menu.pre_render()
                self.manage_team_menu.picked_index = None
            case "save":
                self.save_menu.selected_index = 0
            case "save_confirm" | "quit" | "delete_save" | "launch_battle_confirm":
                self.confirm_action_menu.selected_index = 1
            case "main_launch_menu" | _:
                self.main_launch_menu.selected_index = 0
    
    def check_game_status(self):
        if len(self.player_pokedex.player_team) == 0:
            return "lost_game"
        else:
            return "main_launch_menu"

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking launched menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True
        self.options_menu_event_dict[self.menu_state](event)
            
    def get_event_lost_game(self, event):
        if self.pressed_keys[pg.key.key_code(self.delete_save_keys[0])] \
            and self.pressed_keys[pg.key.key_code(self.delete_save_keys[1])] \
                and self.pressed_keys[pg.key.key_code(self.delete_save_keys[2])]:
            self.menu_effects_channel.play(self.menues_sounds["back"])
            self.update_options("delete_save")
        elif event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_effects_channel.play(self.menues_sounds["back"])
                self.menu_state = "quit"

    def get_event_main_launch_menu(self, event):
        """
        Handles user input in the "main_launch_menu" state.
        Allows navigation and selection of menu options.
        """
        if self.pressed_keys[pg.key.key_code(self.delete_save_keys[0])] \
            and self.pressed_keys[pg.key.key_code(self.delete_save_keys[1])] \
                and self.pressed_keys[pg.key.key_code(self.delete_save_keys[2])]:
            self.menu_effects_channel.play(self.menues_sounds["back"])
            self.update_options("delete_save")
        elif event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys\
                    and not self.quit:
                self.menu_effects_channel.play(self.menues_sounds["back"])
                self.update_options("quit")
            elif pg.key.name(event.key) in self.confirm_keys:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.update_options(self.main_launch_menu.next_list\
                    [self.main_launch_menu.selected_index])
        self.main_launch_menu.get_event_vertical(event)

    def get_event_manage_team(self, event):
        """
        Handles user input in the "manage_team" menu.
        Allows switching Pokémon in the team.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and\
                    not self.quit:
                self.menu_effects_channel.play(self.menues_sounds["back"])
                self.update_options("main_launch_menu")
            elif pg.key.name(event.key) in self.confirm_keys:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                if type(self.manage_team_menu.picked_index) != int:
                    self.manage_team_menu.picked_index = \
                    self.manage_team_menu.selected_index
                else:
                    self.player_pokedex.switch_pokemon(
                        self.manage_team_menu.picked_index,
                        self.manage_team_menu.selected_index
                    )
                    self.update_options("manage_team")
                    self.manage_team_menu.picked_index = None
        self.manage_team_menu.get_event_vertical(event)
    
    def get_event_pokedex_menu(self, event):
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not\
                    self.quit:
                self.menu_effects_channel.play(self.menues_sounds["back"])
                self.update_options("main_launch_menu")
            elif pg.key.name(event.key) in self.confirm_keys:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                selected_entry = self.player_pokedex.pokemon_dict[
                    list(self.player_pokedex.pokemon_dict.keys())[
                        int(self.player_pokedex.pokedex[self.display_pokedex_menu.selected_index])-1
                        ]
                ]["entry"]
                if self.focused_pokemon == selected_entry:
                    self.focused_pokemon = None
                else:
                    self.focused_pokemon = selected_entry
        self.display_pokedex_menu.get_event_vertical(event)

    def get_event_save(self, event):
        """
        Handles user input in the "save" menu.
        Allows selection between saving, exiting, or confirming save.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and not self.quit:
                self.menu_effects_channel.play(self.menues_sounds["back"])
                self.update_options("main_launch_menu")
            elif pg.key.name(event.key) in self.confirm_keys and \
                    self.save_menu.selected_index == 2:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.update_options("main_launch_menu")
            elif pg.key.name(event.key) in self.confirm_keys and \
                    self.save_menu.selected_index in (0,1):
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.update_options("save_confirm")
        self.save_menu.get_event_vertical(event)

    def get_event_save_confirm(self, event):
        """
        Handles user input in the "save_confirm" menu.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and\
                    not self.quit:
                self.menu_effects_channel.play(self.menues_sounds["back"])
                self.update_options("main_launch_menu")
            elif pg.key.name(event.key) in self.confirm_keys and\
                    self.confirm_action_menu.selected_index == 1:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.update_options("main_launch_menu")
            elif pg.key.name(event.key) in self.confirm_keys and\
                    self.confirm_action_menu.selected_index == 0:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.update_options("main_launch_menu")
                player_data = self.player_pokedex.compress_data(str(self.save_menu.selected_index + 1))
                self.save_player_data(player_data, str(self.save_menu.selected_index + 1))
                self.effects_channel.play(self.menues_sounds["save success"])
        self.confirm_action_menu.get_event_vertical(event)
    
    def get_event_delete_save(self, event):
        """
        Handles user input in the "delete_save" menu.
        Allows user to confirm or cancel save deletion.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and\
                    not self.quit:
                self.update_options(self.check_game_status())
            elif pg.key.name(event.key) in self.confirm_keys and\
                    self.confirm_action_menu.selected_index == 1:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.update_options(self.check_game_status())
            elif pg.key.name(event.key) in self.confirm_keys and self.confirm_action_menu.selected_index == 0:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.next = "title_menu"
                self.done = True
                if bool(self.player_pokedex.save):
                    self.reset_player_data(self.player_pokedex.save)
                else:
                    self.next = "title_menu"
                    self.done = True
        self.confirm_action_menu.get_event_vertical(event)

    def get_event_launch_battle_confirm(self, event):
        
        """
        Handles user input in the "launch_battle_confirm" menu.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and\
                    not self.quit:
                self.update_options("main_launch_menu")
            elif pg.key.name(event.key) in self.confirm_keys:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.next = "in_battle"
                self.done = True
                self.launch_battle()
                self.music_channel.stop()
        self.launch_battle_menu.get_event_vertical(event)

    def get_event_quit(self, event):
        """
        Handles user input in the "quit" menu.
        """
        if event.type == pg.KEYDOWN:
            if pg.key.name(event.key) in self.return_keys and\
                    not self.quit:
                self.update_options(self.check_game_status())
            elif pg.key.name(event.key) in self.confirm_keys and\
                    self.confirm_action_menu.selected_index == 1:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.update_options(self.check_game_status())
            elif pg.key.name(event.key) in self.confirm_keys and\
                  self.confirm_action_menu.selected_index == 0:
                self.menu_effects_channel.play(self.menues_sounds["confirm"])
                self.next = "title_menu"
                self.done = True
        self.confirm_action_menu.get_event_vertical(event)