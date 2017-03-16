import pygame

from Enemy.enemy import Enemy
from Level.bullet import Bullet


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

        bullet = Bullet()
        bullet.rect.x = self.rect.x
        bullet.rect.y = self.rect.y
        # bullet.change_x = 6.3 * maths.cos(self.angle)
        # bullet.change_y = 6.3 * maths.sin(self.angle)
        self.bullet_list.add(bullet)

    def go_left(self):
        super().left(self.speed)

    def go_right(self):
        super().right(self.speed)