import pygame

from classes.constants import *


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([10, 3])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += self.add_x
        self.rect.y += self.add_y
        # Need to add direction
