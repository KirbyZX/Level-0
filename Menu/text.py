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
        self.colour = colour
        self.text = text
        self.size = size
        self.style = "Courier New"

        pygame.font.init()
        self.font = pygame.font.SysFont(self.style, size)
        self.image = self.font.render(text, False, colour)
        self.rect = self.image.get_rect()
