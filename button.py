import pygame

from constants import *


class Button(pygame.sprite.Sprite):
    """
    Button the user clicks.
    """

    def __init__(self, text, game):
        """ Button constructor. """

        super().__init__()

        self.game = game

        self.width = game.unit_width
        self.height = game.unit_height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)

        pygame.font.init()
        font = pygame.font.SysFont("Agency FB", 30)
        self.text = font.render(text, False, (0, 0, 0))

        self.rect = self.image.get_rect()
