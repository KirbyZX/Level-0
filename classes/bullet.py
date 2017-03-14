import pygame

from classes.constants import *


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet.
    """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([10, 3])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        pp=[player.rect.x, player.rect.y]
        bullet.rect.x+=bullet.add_x
        bullet.rect.y+=bullet.add_y
        bullet.rect.y+=gravity_acceleration
        if pp[0]<b[0]<pp[0]+20 and pp[1]+30<b[1]<pp[1]+84:  # SHOT!
            player.hp -= 36
            k[bullet.shotby] += [bullet.shotat, bullet.shotat]
            bullet.remove(bullet)
        if pp[0]+20<b[0]<pp[0]+50 and pp[1]+30<b[1]<pp[1]+84:  # SHOT!
            player.hp -= 12
            k[bullet.shotby] += [bullet.shotat]
            bullet.remove(bullet)
        elif [b[0] - b[0] % 50, b[1] - b[1] % 50] in platform_list:
            bullets.remove(bullet)
            if bullet.shotat in k[bullet.shotby]: k[b[5]].remove(b[4])
        # Need to add direction
