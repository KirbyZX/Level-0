import pygame

from classes.constants import *


class Enemy(pygame.sprite.Sprite):
    """
    General class to represent enemies
    """

    def __init__(self, player):
        """ Constructor """

        super().__init__()

        self.change_x = 0
        self.change_y = 0

        self.level = None
        self.player = player

        self.direction = "R"

        # Add image-related stuff here
        width = 70
        height = 84
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

    def update(self):
        """ Moving the enemy """

        self.calc_grav()

        self.rect.x += self.change_x

        # Add animation of images

        # Add AI

        # Checking collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        """ Calculate gravity """

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ AI controlled action """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        """ AI controlled action """

        self.change_x = -7
        self.direction = "L"

    def go_right(self):
        """ AI controlled action """

        self.change_x = -7
        self.direction = "R"

    def stop(self):
        """ AI controlled action """

        self.change_x = 0
