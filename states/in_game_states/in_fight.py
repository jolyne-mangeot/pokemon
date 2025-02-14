import pygame as pg
from control.states_control import States
from states.in_game_states.__game_menu_manager__ import Game_menu_manager
from states.in_game_states.__in_fight_states__ import In_fight_states

pg.font.init()

class In_fight(States, Game_menu_manager, In_fight_states):
    def __init__(self):
        States.__init__(self)
        Game_menu_manager.__init__(self)
        self.next = "launch_menu"
        self.back = "launch_menu"

    def cleanup(self):
        """
        cleans up all menu related data
        """
        self.fight.player_pokedex.encounters["done"] +=1
        self.unload_graphics_pokemons()

    def startup(self):
        """
        initiates all menu related data
        """
        self.fight = States.new_fight
        self.menu_state = "battle_stage"
        self.update_options()
        self.fight.spawn_pokemon(0, True)
        self.fight.spawn_pokemon(0, False)
        self.load_graphics_pokemons()

    def get_event(self, event):
        """
            get all pygame-related events proper to the menu before
            checking main menu shared events
        """
        if event.type == pg.QUIT:
            self.quit = True

        match self.menu_state:
        #     case "display_items":
        #         if self.get_event_launch_fight_confirm(event):
        #             self.launch_fight()
        #         self.get_event_confirm(event)
            case "display_team":
                self.get_event_display_team(event)
                self.get_event_menu(event)
            case "select_pokemon_confirm":
                if self.get_event_select_pokemon_confirm(event):
                    self.fight.spawn_pokemon(self.chosen_pokemon, True)
                self.get_event_menu(event)
            case "quit":
                self.back = "battle_stage"
                self.get_event_run_away(event)
                self.get_event_menu(event)
            case "battle_stage" | _:
                self.get_event_battle_stage(event)
                self.get_event_menu(event)
   
    def update(self):
        self.draw()
    
    def draw(self):
        self.screen.fill((0,0,255))
        self.draw_pokemons()
        self.draw_pokemons_health_points()
        match self.menu_state:
            case "battle_stage":
                self.draw_menu_options()
            case "quit":
                self.draw_menu_options()
            case "display_team" | "select_pokemon_confirm":
                self.draw_menu_options()
