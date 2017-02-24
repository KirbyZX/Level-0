import pygame
from level_zero.constants import *
from level_zero.player import Player
from level_zero.bullet import Bullet
from level_zero.level_01 import *
from level_zero.level_02 import *


def main():
    """ Main Program """

    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Level Zero")
    pygame.display.set_icon(pygame.transform.scale(pygame.image.load("player_run/run0.png").convert_alpha(), [32, 32]))

    # Create the player
    player = Player()

    # Create all the levels
    level_list = [Level_01(player), Level_02(player)]

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop --------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    # Fire a bullet if the user clicks the mouse button
                    bullet = Bullet()
                    # Set the bullet so it is where the player is
                    bullet.rect.x = player.rect.x + 35
                    bullet.rect.y = player.rect.y + 10
                    # Add the bullet to the lists
                    active_sprite_list.add(bullet)
                    level_list[current_level_no].bullet_list.add(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        for bullet in level_list[current_level_no].bullet_list:

            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, level_list[current_level_no].platform_list, False)

            # For each block hit, remove the bullet
            for _ in block_hit_list:
                level_list[current_level_no].bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

            # Remove the bullet if it flies up off the screen
            if bullet.rect.x > SCREEN_WIDTH + 10 or bullet.rect.x < -10:
                level_list[current_level_no].bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 750:
            diff = player.rect.right - 750
            player.rect.right = 750
            current_level.scroll(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 250:
            diff = 250 - player.rect.left
            player.rect.left = 250
            current_level.scroll(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.level_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list) - 1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        # ALL CODE TO DRAW SHOULD GO BELOW
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE

        # Limit to 60 frames per second
        clock.tick(60)

        # Update the screen with what we've drawn.
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
