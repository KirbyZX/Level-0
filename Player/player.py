import pygame

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

        # Dimensions of player
        width = 70
        height = 84

        path = "C:/Users/lucas.LUCAS/Google Drive/Python/Level-0/images/"

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

        # Health points
        self.hp = 100

    def update(self):
        """ Moving the player. """

        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # Player position
        pos = self.rect.x + self.level.level_shift

        # Animating
        if self.direction == "R" and self.change_x != 0:
            frame = (pos // 20) % len(self.running_frames_r)
            self.image = self.running_frames_r[frame]
        elif self.change_x != 0:
            frame = (pos // 20) % len(self.running_frames_l)
            self.image = self.running_frames_l[frame]
        else:
            if self.direction == "R":
                self.image = self.stand
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

    def calc_grav(self):
        """ Calculate effect of gravity. """

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # Check if there is a platform below us
        # Move down 2 pixels because it doesn't work well if we only move down 1
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.y -= 2

        # If able to jump, go up
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:

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
