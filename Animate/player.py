import pygame
import time
import math

from Level.block_moving import MovingBlock
from Level.platform import Platform
from constants import *


class Player(pygame.sprite.Sprite):
    """
    Generic class for defining the player.
    """

    def __init__(self, game):
        """ Constructor """

        super().__init__()

        # Reference to game for screen ratios
        self.game = game

        # Speed vectors
        self.change_x = 0
        self.change_y = 0

        # Reference to level for collisions
        self.level = None

        # Direction
        self.direction = "R"

        # Hit points
        self.hp = 100

        # Dash control
        self.dashing = False
        self.dash_time = time.time()

        # Mouse
        self.mouse = [0, 0]

        # Energy
        self.energy = 100

        # Jump count
        self.jump_count = 2

        # Reverse gravity
        self.reverse_gravity = False

        # Handling automatic shooting
        self.cooldown = 0.5
        self.shot_time = 0
        self.shooting = False

        # Image - acts as hit box
        width = int(game.unit_width * 2)
        height = int(game.unit_height * 2)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        """ Moving the character """

        # Gravity
        if not self.dashing:
            self.calc_gravity()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0 and not isinstance(block, Platform):
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingBlock):
                self.rect.x += block.change_x

        # Energy regeneration
        self.energy += .2
        if self.energy > 100:
            self.energy = 100
        if self.energy < 0:
            self.energy = 0

        # Check if there is a platform below us
        # Move down 2 pixels because it doesn't work well if we only move down 1
        if not self.reverse_gravity:
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
            self.rect.y -= 2
        else:
            self.rect.y -= 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
            self.rect.y += 2
        # Reset jump count
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.game.screen_height \
                or (self.rect.top <= 0 and self.reverse_gravity):
            self.jump_count = 2

    def calc_gravity(self):
        """ Calculating gravity """

        if self.change_y == 0:
            if self.reverse_gravity:
                self.change_y = -1
            else:
                self.change_y = 1
        else:
            if self.reverse_gravity:
                self.change_y += -.35
            else:
                self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= self.game.screen_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.game.screen_height - self.rect.height
        # See if we are on the ceiling
        if self.rect.y <= 0 and self.change_y <= 0:
            self.change_y = 0
            self.rect.y = 0

    # User controlled movement:

    def jump(self):
        """ Character jumps """

        if self.jump_count > 0:
            if not self.reverse_gravity:
                self.change_y = -10
            else:
                self.change_y = 10
            self.jump_count -= 1

    def go_left(self):
        """ Called when the user hits the left arrow. """

        self.change_x = -7
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """

        self.change_x = 7
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """

        self.change_x = 0

    def dash(self):
        """ Moves the player towards the mouse. """

        self.dash_time = time.time()
        print(self.mouse[0])
        print(self.rect.x)
        diff_x = self.mouse[0] - self.rect.x
        diff_y = self.mouse[1] - self.rect.y
        # Preventing division by zero
        if diff_x == 0:
            diff_x = 1
        # Calculating the angle
        velocity = 15
        angle = math.atan(diff_y / diff_x)
        if diff_x < 0:
            angle = math.pi - angle
            angle *= -1
        # Calculating movement
        self.dashing = True
        self.dash_time = time.time()
        self.energy -= 25
        self.change_x = velocity * math.cos(angle)
        self.change_y = velocity * math.sin(angle)
