import pygame
import math as maths

from constants import *


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet.
    """

    def __init__(self, target):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([5, 5])
        self.image.fill(BLACK)

        self.target = target

        self.change_x = 0
        self.change_y = 0

        self.rect = self.image.get_rect()

    def calculate(self):
        """ Calculate angle and velocity. """

        diff_x = self.target[0] - self.rect.x
        diff_y = self.target[1] - self.rect.y
        # Preventing division by zero
        if diff_x == 0:
            diff_x = 1
        # Calculating the angle
        angle = maths.atan(diff_y / diff_x)
        if diff_x < 0:
            angle = maths.pi - angle
            angle *= -1
        # Calculating movement
        self.change_x = 20 * maths.cos(angle)
        self.change_y = 20 * maths.sin(angle)

    def update(self):
        """ Move the bullet. """

        self.rect.x += self.change_x
        self.rect.y += self.change_y
