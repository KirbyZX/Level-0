import pygame

from Animate.ai import ai
from constants import *

info={}
eInfo=open("enemies", "r")
eInfoL=eInfo.readlines()
for e in eInfoL:
    e=e.split("\\")
    e=e[0]
    e=e.split(":")
    Ename=e[0]
    Einfo=e[1]
    Einfo=Einfo.split(",")
    for i in Einfo:
        ii=Einfo.index(i)
        try:
            i=float(i)
        except ValueError:
            i=i.split("-")
            for eye in i:
                eyei=i.index(eye)
                try: eye=float(eye)
                except ValueError: eye=str(eye)
                i[eyei]=eye
        Einfo[ii]=i
    info[Ename]=Einfo

class Enemy(pygame.sprite.Sprite):
    """
    General class to represent enemies.
    """

    def __init__(self, player):
        """ Constructor """

        super().__init__()

        self.change_x = 0
        self.change_y = 0

        self.level = None
        self.player = player

        self.direction = "R"
        self.angle = 0

        # Add image-related stuff here
        width = 70
        height = 84
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()

    def update(self, player):
        """ Moving the enemy """

        self.calc_gravity()

        self.rect.x += self.change_x
        
        # self.angle=maths.atan((self.rect.y-player.rect.y)/(self.rect.x-player.rect.x)) #face towards the player

        # Add animation of images

        # AI
        ai(self, self.player, 20)

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

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ AI controlled action """

        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def left(self):
        """ AI controlled action """

        self.change_x = -self.speed
        self.direction = "L"

    def right(self):
        """ AI controlled action """

        self.change_x = self.speed
        self.direction = "R"

    def stop(self):
        """ AI controlled action """

        self.change_x = 0
