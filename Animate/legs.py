import pygame

from Animate.player import Player
from Level.block_moving import MovingBlock
from Level.platform import Platform


class Legs(pygame.sprite.Sprite):
    """
    Represents the main character of the game which the player controls.
    """

    def __init__(self, character, game):
        """ Constructor """

        # Calling the parent's constructor
        super().__init__()

        self.character = character

        # Lists that hold the running frames
        self.running_frames_l = []
        self.running_frames_r = []

        # Dimensions of player
        width = int(game.unit_width * 2)
        height = int(game.unit_height * 2)

        path = "D:/Users/lucas.Lucas/Google Drive/Python/Level-0/.images/run/"

        if isinstance(self.character, Player):

            # Standing image
            self.stand = pygame.transform.scale(pygame.image.load(path + "stand.png").convert_alpha(), [width, height])

            # Right-facing images
            for n in range(0, 8):
                image = pygame.transform.scale(pygame.image.load(path+"run"+str(n)+".png").convert_alpha(), [width, height])
                self.running_frames_r.append(image)

            # Left-facing images
            for n in range(0, 8):
                image = pygame.transform.scale(pygame.image.load(path+"run"+str(n)+".png").convert_alpha(), [width, height])
                image = pygame.transform.flip(image, True, False)
                self.running_frames_l.append(image)

        # Starting image
        self.image = self.running_frames_r[0]
        self.frame_count = 0

        # Image rectangle for collision
        self.rect = self.image.get_rect()

    def update(self):
        """ Updating based on the player """

        # Movement along x-axis
        self.rect.x = self.character.rect.x

        # Animating
        if self.character.direction == "R" and self.character.change_x != 0:
            if self.frame_count >= len(self.running_frames_r) - 1:
                self.frame_count = 0
            else:
                self.frame_count = self.frame_count + 0.5
            if self.character.reverse_gravity:
                self.image = pygame.transform.flip(self.running_frames_r[int(self.frame_count)], False, True)
            else:
                self.image = self.running_frames_r[int(self.frame_count)]
        elif self.character.change_x != 0:
            if self.frame_count >= len(self.running_frames_r) - 1:
                self.frame_count = 0
            else:
                self.frame_count = self.frame_count + 0.5
            if self.character.reverse_gravity:
                self.image = pygame.transform.flip(self.running_frames_l[int(self.frame_count)], False, True)
            else:
                self.image = self.running_frames_l[int(self.frame_count)]
        else:
            if self.character.direction == "R":
                if self.character.reverse_gravity:
                    self.image = pygame.transform.flip(self.stand, False, True)
                else:
                    self.image = self.stand
            else:
                if self.character.reverse_gravity:
                    self.image = pygame.transform.flip(pygame.transform.flip(self.stand, True, False), False, True)
                else:
                    self.image = pygame.transform.flip(self.stand, True, False)

        # Movement along y-axis
        self.rect.y = self.character.rect.y
