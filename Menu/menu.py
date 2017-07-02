import pygame

from constants import *


class Menu:
    """
    Super-class to define a menu with buttons etc.
    Create a child class for each menu with menu-specific info.
    """

    def __init__(self, game):
        """ Constructor """

        self.button_list = pygame.sprite.Group()
        self.text_list = pygame.sprite.Group()
        self.game = game

    def draw(self, screen):

        screen.fill(BLACK)

        self.button_list.draw(screen)
        self.text_list.draw(screen)
