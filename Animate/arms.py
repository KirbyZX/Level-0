import pygame

from Animate.player import Player
from Level.block_moving import MovingBlock
from Level.platform import Platform


class Arms(Player):
    """
    Represents the main character of the game which the player controls.
    """

    def __init__(self, game):
        """ Constructor """

        # Calling the parent's constructor
        super().__init__(game)

        # Lists that hold the running frames
        self.shooting_frames_l = []
        self.shooting_frames_r = []

        # Dimensions of player
        width = int(game.unit_width * 2)
        height = int(game.unit_height * 2)

        path = "D:/Users/lucas.Lucas/Google Drive/Python/Level-0/.images/shoot/"

        self.still = pygame.transform.scale(pygame.image.load(path + "shoot0.png").convert_alpha(), [width, height])

        # Right-facing images
        for n in range(0, 8):
            image = pygame.transform.scale(pygame.image.load(path+"shoot"+str(n)+".png").convert_alpha(), [width, height])
            self.shooting_frames_r.append(image)

        # Left-facing images
        for n in range(0, 8):
            image = pygame.transform.scale(pygame.image.load(path+"shoot"+str(n)+".png").convert_alpha(), [width, height])
            image = pygame.transform.flip(image, True, False)
            self.shooting_frames_l.append(image)

        # Starting image
        self.image = self.still
        self.frame_count = 0

        # Image rectangle for collision
        self.rect = self.image.get_rect()

        # Handling automatic shooting
        self.cooldown = 0.1
        self.shot_time = 0
        self.shooting = False

    def update(self):
        """ Moving the player. """

        super().update()

        # Animating

        if self.direction == "R" and self.shooting:
            if self.frame_count >= len(self.shooting_frames_r) - 1:
                self.frame_count = 0
            else:
                self.frame_count = self.frame_count + 0.5
            if self.reverse_gravity:
                self.image = pygame.transform.flip(self.shooting_frames_r[int(self.frame_count)], False, True)
            else:
                self.image = self.shooting_frames_r[int(self.frame_count)]
        elif self.shooting:
            if self.frame_count >= len(self.shooting_frames_r) - 1:
                self.frame_count = 0
            else:
                self.frame_count = self.frame_count + 0.5
            if self.reverse_gravity:
                self.image = pygame.transform.flip(self.shooting_frames_l[int(self.frame_count)], False, True)
            else:
                self.image = self.shooting_frames_l[int(self.frame_count)]
        else:
            if self.direction == "R":
                if self.reverse_gravity:
                    self.image = pygame.transform.flip(self.stand, False, True)
                else:
                    self.image = self.still
            else:
                if self.reverse_gravity:
                    self.image = pygame.transform.flip(pygame.transform.flip(self.stand, True, False), False, True)
                else:
                    self.image = pygame.transform.flip(self.still, True, False)

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

    def calc_gravity(self):

        super().calc_gravity()

    # Player-controlled movement:

    def jump(self):

        super().jump()

    def go_left(self):

        super().go_left()

    def go_right(self):

        super().go_right()

    def stop(self):

        super().stop()

    def dash(self):

        super().dash()
