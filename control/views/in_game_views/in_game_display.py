import pygame as pg

from control.views.display import Display

class In_game_display(Display):
    def init_in_game_display(self):
        Display.__init__(self)
        self.init_root_variables_in_game()
        self.load_graphics_launch_menues()
        self.load_graphics_pokemons()

    def init_root_variables_in_game(self):
        width : int = self.screen_rect.width
        height : int = self.screen_rect.height

        self.active_pokemon_image_size : tuple = (width*0.3, width*0.3)
        self.mini_image_size : tuple = (width*0.21, width*0.2)

    def load_graphics_pokemons(self):
        for pokemon in self.player_pokedex.player_team:
            back_image = pg.image.load(self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/back.png")
            pokemon.back_image = pg.transform.scale(back_image, self.active_pokemon_image_size)
            mini_image = pg.image.load(self.GRAPHICS_PATH + "pokemon/" + pokemon.entry + "/mini.png")
            pokemon.mini_image = pg.transform.scale(mini_image, self.mini_image_size)

    def init_render_option_team(self, team, forced_switch=False, team_full=False):
        options = []
        for pokemon in team:
            options.append(self.dialogs[pokemon.name])
        while len(options) < 6:
            options.append("")
        if not forced_switch and not team_full:
            options.append(self.dialogs['back'])
        return options

    def draw_precombat_field(self):
        pg.transform.scale(self.field,(self.screen_width, self.screen_height))
        self.screen.blit(self.field,(0,0))
        
    def draw_combat_screen(self):
        pg.transform.scale(self.field,(self.screen_width, self.screen_height))
        self.screen.blit(self.field,(0,0))

    def load_graphics_launch_menues(self):
        self.launch_menu_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"launch screen.png")
        self.launch_menu_img=pg.transform.scale(self.launch_menu_img, (self.screen_width,self.screen_height))

        self.pkmn_frame_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pkmn frame.png")
        self.pkmn_frame_img=pg.transform.scale(self.pkmn_frame_img, (self.screen_width,self.screen_height))

        self.team_select_img=pg.image.load(self.GRAPHICS_PATH+"/media/"+"pkmn frame.png")
        self.team_select_img=pg.transform.scale(self.team_select_img, (self.screen_width,self.screen_height))
    
    def draw_launch_menu(self):
        self.launch_menu_img=pg.transform.scale(self.launch_menu_img, (self.screen_width,self.screen_height))
        self.screen.blit(self.launch_menu_img,(0,0))
    
    def draw_pkmn_frame(self):
        self.pkmn_frame_img=pg.transform.scale(self.pkmn_frame_img, (self.screen_width,self.screen_height))
        self.screen.blit(self.pkmn_frame_img,(0,0))
    
    def draw_team_select_img(self):
        self.team_select_img=pg.transform.scale(self.team_select_img, (self.screen_width,self.screen_height))
        self.screen.blit(self.team_select_img,(0,0))