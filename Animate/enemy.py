import pygame
import random

from Animate.ai import ai
from constants import *


class Enemy(pygame.sprite.Sprite):
    """
    General class to represent enemies.
    """

    def __init__(self, player, game):
        """ Constructor """

        self.game = game

        super().__init__()

        self.change_x = 0
        self.change_y = 0

        self.health = 100
        self.dead = False

        self.level = None
        self.player = player

        self.direction = "R"
        self.angle = 0

        self.random = random.randrange(150, 250)

        # Add image-related stuff here
        width = int(game.unit_width)
        height = int(game.unit_height * 2)
        self.image = pygame.Surface([width, height])
        self.image.fill(random.choice(list_of_colours))

        self.rect = self.image.get_rect()

    def update(self, player):
        """ Moving the enemy """

        self.calc_gravity()

        self.rect.x += self.change_x
        
        # self.angle=maths.atan((self.rect.y-player.rect.y)/(self.rect.x-player.rect.x)) #face towards the player

        # Add animation of images

        # AI
        ai(self, self.player, self.random)

        # Checking collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_gravity(self):
        """ Calculate gravity """

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= self.game.screen_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.game.screen_height - self.rect.height

    def jump(self):
        """ AI controlled action """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= self.game.screen_height:
            self.change_y = -10

    def left(self, speed):
        """ AI controlled action """

        self.change_x = -speed
        self.direction = "L"

    def right(self, speed):
        """ AI controlled action """

        self.change_x = speed
        self.direction = "R"

    def stop(self):
        """ AI controlled action """

        self.change_x = 0

    def die(self):
        """ When health <= 0 """

        self.image.fill(BLACK)
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.stop()
        self.dead = True
