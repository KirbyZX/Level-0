import pygame

from classes.constants import *


class Platform(pygame.sprite.Sprite):
    """
    Platform the user can jump on.
    """

    def __init__(self, width, height):
        """ Platform constructor. Assumes user passing in an array of 5 numbers. """

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
