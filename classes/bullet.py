import pygame

from constants import *


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet.
    """

    def __init__(self, thing):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([10, 3])
        self.image.fill(BLACK)

        self.direction = thing.direction

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        if self.direction == "R":
            self.rect.x += 15
        else:
            self.rect.x -= 15
        # Need to add direction
