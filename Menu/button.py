import pygame

from constants import *


class Button(pygame.sprite.Sprite):
    """
    Button the user clicks.
    """

    def __init__(self, width, height, text, game):
        """ Button constructor. """

        super().__init__()

        self.game = game
        self.text = text

        self.width = width * game.unit_width
        self.height = height * game.unit_height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
