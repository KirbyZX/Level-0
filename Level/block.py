import pygame

from constants import *


class Block(pygame.sprite.Sprite):
    """
    Platform the player can jump on.
    """

    def __init__(self, game):
        """ Platform constructor. """

        super().__init__()

        self.game = game

        self.width = game.unit_width
        self.height = game.unit_height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
