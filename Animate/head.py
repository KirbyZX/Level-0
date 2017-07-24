import pygame
import math

from constants import *
from Animate.player import Player


class Head(pygame.sprite.Sprite):
    """
    The head of the player.
    """

    def __init__(self, character, mouse, game):

        super().__init__()

        self.character = character
        self.mouse = mouse

        width = int(game.unit_width)
        height = int(game.unit_height)

        path = "D:/Users/lucas.Lucas/Google Drive/Python/Level-0/.images/"

        if isinstance(self.character, Player):
            self.image = pygame.transform.scale(pygame.image.load(path + "head.png"), [width, height])
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        """ Updating based on the player """

        # Animating (still need rotation)
        if self.character.direction == "R":
            self.rect.center = self.character.rect.topright
        else:
            self.rect.center = self.character.rect.topleft

        if self.character.change_x == 0:
            self.rect.centerx = self.character.rect.centerx
