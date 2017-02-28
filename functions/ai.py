import pygame


def ai(enemy, player):
    """ Basic A.I. for enemies """

    if enemy.rect.x > player.rect.x + 200:
        enemy.go_left()
    elif enemy.rect.x < player.rect.x - 200:
        enemy.go_right()
    else:
        enemy.stop()

    if enemy.rect.y < player.rect.y:
        enemy.jump()

    enemy.rect.x += 2
    platform_hit_list = pygame.sprite.spritecollide(enemy, enemy.level.platform_list, False)
    enemy.rect.x -= 2
    if len(platform_hit_list) > 0:
        enemy.jump()

    enemy.rect.x -= 2
    platform_hit_list = pygame.sprite.spritecollide(enemy, enemy.level.platform_list, False)
    enemy.rect.x += 2
    if len(platform_hit_list) > 0:
        enemy.jump()
