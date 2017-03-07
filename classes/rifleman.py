import pygame

from classes.enemy import Enemy
from classes.bullet import Bullet


class Rifleman(Enemy):
    """
    Child class of Enemy to represent
    a basic rifleman.
    """

    def __init__(self, player):
        """ Constructing the enemy """

        # Parent constructor
        Enemy.__init__(self, player)

        self.hp = 24
        self.speed = 5

        self.bullet_list = pygame.sprite.Group()

    def shoot(self):
        """ Shooting a bullet """

        bullet = Bullet(self)
        bullet.rect.x = self.rect.x
        bullet.rect.y = self.rect.y

        self.bullet_list.add(bullet)

    def go_left(self):
        super().left(self.speed)

    def go_right(self):
        super().right(self.speed)
