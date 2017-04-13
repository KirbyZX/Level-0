import pygame

from constants import *


class Platform(pygame.sprite.Sprite):
    """
    Platform that can be jumped on from underneath
    """

    def __init__(self):
        """ Platform constructor. """

        super().__init__()

        self.image = pygame.Surface([50, 10])
        self.image.fill(MAGENTA)

        self.rect = self.image.get_rect()
