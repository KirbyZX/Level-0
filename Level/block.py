import pygame

from constants import *


class Block(pygame.sprite.Sprite):
    """
    Platform the user can jump on.
    """

    def __init__(self):
        """ Platform constructor. Assumes user passing in an array of 5 numbers. """

        super().__init__()

        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
