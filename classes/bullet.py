import pygame

from constants import *


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([10, 3])
        self.image.fill(BLACK)

        self.change_x = 15

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """

        self.rect.x += self.change_x
        # Jack, you put the getting shot part in the main loop
