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
