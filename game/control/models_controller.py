import pygame as pg
import abc

from game.control.control import Control

class Models_controller(Control, abc.ABC):
    """
    Base controller class for handling game models. 
    This class serves as an abstract controller for managing different game states and interactions.
    """
    def __init__(self):
        Control.init_config(self)
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None

    player_pokedex = None
    new_battle = None

    
    @abc.abstractmethod
    def startup(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def cleanup(self):
        pass