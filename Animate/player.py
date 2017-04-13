import pygame
import math as maths
import time

from Level.block_moving import MovingBlock
from Level.platform import Platform
from constants import *


class Player(pygame.sprite.Sprite):
    """
    Represents the main character of the game which the player controls.
    """

    def __init__(self):
        """ Constructor """

        # Calling the parent's constructor
        super().__init__()

        # Speed vectors of player
        self.change_x = 0
        self.change_y = 0

        # List of sprites the player can collide with
        self.level = None

        # Direction of the player
        self.direction = "R"

        # Lists that hold the running frames
        self.running_frames_l = []
        self.running_frames_r = []

        # Dimensions of player (fat)
        width = 70
        height = 84

        path = "C:/Users/lucas.Lucas/Google Drive/Python/Level-0/.images/"

        self.stand = pygame.transform.scale(pygame.image.load(path + "stand.png").convert_alpha(), [width, height])

        # Right-facing images
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run0.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run1.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run2.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run3.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run4.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run5.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run6.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run7.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run8.png").convert_alpha(), [width, height])
        self.running_frames_r.append(image)

        # Left-facing images
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run0.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run1.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run2.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run3.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run4.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run5.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run6.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run7.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)
        image = pygame.transform.scale(pygame.image.load(path + "player_run/run8.png").convert_alpha(), [width, height])
        image = pygame.transform.flip(image, True, False)
        self.running_frames_l.append(image)

        # Starting image
        self.image = self.stand

        # Image rectangle for collision
        self.rect = self.image.get_rect()

        # Hit points
        self.hp = 100

        # Dash control:   dashing?, dash time,   x, y
        self.dash_list = [False,    time.time(), 0, 0]

        self.mouse = []

        # Energy
        self.energy = 100

        # Handling automatic shooting
        self.cooldown = 0.1
        self.shot_time = 0
        self.shooting = False

        self.jump_count = 2

        # Reverse gravity
        self.reverse_gravity = False

    def update(self):
        """ Moving the player. """

        # Gravity

        if not self.dash_list[0]:
            self.calc_gravity()

        # Move left/right
        self.rect.x += self.change_x

        # Player position
        pos = self.rect.x + self.level.level_shift

        # Animating
        if self.direction == "R" and self.change_x != 0:
            frame = (pos // 20) % len(self.running_frames_r)
            if self.reverse_gravity:
                self.image = pygame.transform.flip(self.running_frames_r[frame], False, True)
            else:
                self.image = self.running_frames_r[frame]
        elif self.change_x != 0:
            frame = (pos // 20) % len(self.running_frames_l)
            if self.reverse_gravity:
                self.image = pygame.transform.flip(self.running_frames_l[frame], False, True)
            else:
                self.image = self.running_frames_l[frame]
        else:
            if self.direction == "R":
                if self.reverse_gravity:
                    self.image = pygame.transform.flip(self.stand, False, True)
                else:
                    self.image = self.stand
            else:
                if self.reverse_gravity:
                    self.image = pygame.transform.flip(pygame.transform.flip(self.stand, True, False), False, True)
                else:
                    self.image = pygame.transform.flip(self.stand, True, False)

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
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT \
                or (self.rect.top <= 0 and self.reverse_gravity):
            self.jump_count = 2

    def calc_gravity(self):
        """ Calculate effect of gravity. """

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
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
        # See if we are on the ceiling
        if self.rect.y <= 0 and self.change_y <= 0:
            self.change_y = 0
            self.rect.y = 0

    # Player-controlled movement:

    def jump(self):
        """ Called when user hits 'jump' button. """

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

        self.dash_list[1] = time.time()
        diff_x = self.mouse[0] - self.rect.x
        diff_y = self.mouse[1] - self.rect.y
        # Preventing division by zero
        if diff_x == 0:
            diff_x = 1
        # Calculating the angle
        velocity = 10
        angle = maths.atan(diff_y / diff_x)
        if diff_x < 0:
            angle = maths.pi - angle
            angle *= -1
        # Calculating movement
        self.dash_list = [True, time.time(), velocity * maths.cos(angle), velocity * maths.sin(angle)]
        self.energy -= 25
        self.change_x = self.dash_list[2]
        self.change_y = self.dash_list[3]


