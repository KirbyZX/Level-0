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

        self.size = game.screen_width / 24
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
