import pygame as pg
import abc

from control.control import Control

class States(Control, abc.ABC):
    player_pokedex = None
    new_fight = None

    def __init__(self):
        Control.init_config(self)
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None

    @abc.abstractmethod
    def cleanup(self):
        pass
    
    @abc.abstractmethod
    def startup(self):
        pass