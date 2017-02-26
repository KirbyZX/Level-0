import pygame

from classes.constants import *


class Level:
    """
    Generic super-class used to define a level.
    Create a child class for each level with level-specific info.
    """

    def __init__(self, player):
        """ Constructor. Need player parameter for collisions. """

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.player = player

        # How far the level has been scrolled left/right
        self.level_shift = 0

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""

        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(WHITE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def scroll(self, shift_x):
        """ Scrolls when the player moves left or right. """

        # Keep track of the shift amount
        self.level_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for bullet in self.bullet_list:
            bullet.rect.x += shift_x