import time
import pygame

from Animate.player import Player
from Animate.rifleman import Rifleman
from Inanimate.bullet import Bullet
from Level.level_01 import *
from Level.level_02 import *
from constants import *


def main():
    """ Main Program """

    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    # Full screen?
    # resolution = [1920, 1080]
    # screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)

    # Set cursor to cross-hair
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    # Create the objects
    player = Player()
    enemy = Rifleman(player)

    # Set caption and icon
    pygame.display.set_caption("Level Zero")
    pygame.display.set_icon(pygame.transform.scale(player.running_frames_r[0], [32, 32]))

    # Create all the levels
    level_list = [Level_01(player), Level_02(player)]

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    player.level = current_level
    enemy.level = current_level
    enemy.player = player

    active_sprite_list = pygame.sprite.Group()
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    current_level.enemy_list.add(enemy)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    while not done:

        # Mouse position
        mouse_pos = pygame.mouse.get_pos()

        player.mouse = mouse_pos
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                player.shooting = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_h:
                    player.hp -= 10
                if event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_e:
                    if player.energy >= 25:
                        player.dash()
                if event.key == pygame.K_r:
                    player.reverse_gravity = not player.reverse_gravity

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.add(enemy.bullet_list)
        active_sprite_list.update()
        
        # SHOTS FIRED
        if player.shooting and time.time() >= player.shot_time + player.cooldown:
            # Fire a bullet if the user clicks
            bullet = Bullet(mouse_pos)
            # Cooldown calculation code
            player.shot_time = time.time()
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x + 35
            bullet.rect.y = player.rect.y + 10
            bullet.calculate()
            # Add the bullet to the lists
            active_sprite_list.add(bullet)
            level_list[current_level_no].bullet_list.add(bullet)

        # Stopping dashes
        if player.dash_list[0]:
            if time.time() - player.dash_list[1] >= .5:
                player.dash_list[0] = False
                player.stop()

        for bullet in level_list[current_level_no].bullet_list:

            # See if it hit a block
            block_hit_list = pygame.sprite.spritecollide(bullet, level_list[current_level_no].block_list, False)

            # For each block hit, remove the bullet
            for _ in block_hit_list:
                level_list[current_level_no].bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

            # Remove the bullet if it flies up off the screen
            if bullet.rect.x > SCREEN_WIDTH + 10 or bullet.rect.x < -10:
                level_list[current_level_no].bullet_list.remove(bullet)
                active_sprite_list.remove(bullet)

        # Update items in the level
        current_level.update(player)

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

        # Health bar
        pygame.draw.rect(screen, BLACK, [98, 8, 803, 23], 2)  # Outline
        pygame.draw.rect(screen, (255 - int((255 * player.hp / 100) // 1), int((255 * player.hp / 100) // 1), 0),
                         [100, 10, 800 * player.hp / 100, 20])
        # Energy bar
        pygame.draw.rect(screen, BLACK, [98, 33, 503, 13], 2)  # Outline
        pygame.draw.rect(screen, CYAN, [100, 35, 500 * player.energy / 100, 10])
        # ALL CODE TO DRAW SHOULD GO ABOVE

        # Limit to 60 frames per second
        clock.tick(60)

        # Update the screen with what we've drawn.
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
