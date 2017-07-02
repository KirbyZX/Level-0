import pygame

from constants import *


class Text(pygame.sprite.Sprite):
    """
    Displayable text in menus or other.
    """

    def __init__(self, text, size, colour, game):
        """ Text constructor """

        super().__init__()

        self.game = game

        pygame.font.init()
        font = pygame.font.SysFont("Calibri", size)
        self.image = font.render(text, False, colour)
        self.rect = self.image.get_rect()
