import pygame

from Animate.enemy import Enemy
from Inanimate.bullet import Bullet


class Rifleman(Enemy):
    """
    Child class of Enemy to represent
    a basic rifleman.
    """

    def __init__(self, player, game):
        """ Constructing the enemy """

        # Parent constructor
        Enemy.__init__(self, player, game)

        self.hp = 24
        self.speed = 5

        self.bullet_list = pygame.sprite.Group()

    def shoot(self):
        """ Shooting a bullet """

        bullet = Bullet([self.player.rect.x, self.player.rect.y])
        bullet.rect.x = self.rect.x
        bullet.rect.y = self.rect.y
        bullet.calculate()
        self.bullet_list.add(bullet)

    def go_left(self):
        super().left(self.speed)

    def go_right(self):
        super().right(self.speed)
