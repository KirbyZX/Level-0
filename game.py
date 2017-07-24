import time
import pygame

from constants import *
from Menu.start_menu import StartMenu
from Animate.head import Head
from Animate.arms import Arms
from Animate.legs import Legs
from Animate.player import Player
from Animate.rifleman import Rifleman
from Inanimate.bullet import Bullet
from Level.level_01 import Level_01
from Level.level_02 import Level_02


class Game:
    """
    Main game class.
    """

    def __init__(self):
        """ Constructor """

        pygame.init()

        # Screen setup
        self.resolution = pygame.display.list_modes()[0]
        self.screen_width = self.resolution[0]
        self.screen_height = self.resolution[1]
        self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)

        self.unit_width = self.screen_width / 28
        self.unit_height = self.screen_height / 16

        # Personalising
        pygame.display.set_caption("Level Zero")
        # pygame.display.set_icon(pygame.transform.scale("icon", [32, 32]))
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def start(self):
        """ Start menu """

        start_menu = StartMenu(self)

        done = False
        while not done:

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in start_menu.button_list:
                        if button.rect.x < mouse_pos[0] < button.rect.x + button.width and \
                           button.rect.y < mouse_pos[1] < button.rect.y + button.height:
                            if button.text == "Start":
                                done = True
                            if button.text == "Exit":
                                done = True
                                pygame.quit()

            for button in start_menu.button_list:
                for text in start_menu.text_list:
                    if button.rect.x < mouse_pos[0] < button.rect.x + button.width and \
                       button.rect.y < mouse_pos[1] < button.rect.y + button.height:
                        button.image.fill(WHITE)
                        if button.text == text.text:
                            text.font = pygame.font.SysFont(text.style, text.size)
                            text.image = text.font.render(text.text, False, BLACK)
                            break

                    else:
                        button.image.fill(BLACK)
                        text.font = pygame.font.SysFont(text.style, text.size)
                        text.image = text.font.render(text.text, False, WHITE)

            start_menu.draw(self.screen)
            self.clock.tick(60)
            pygame.display.flip()

    def play(self):
        """ Main program """

        # Player creation
        player = Player(self)
        head = Head(player, None, self)
        legs = Legs(player, self)

        # Enemy creation
        enemy = Rifleman(player, self)

        # Create all the levels
        level_list = [Level_01(player, self), Level_02(player, self)]

        # Set the current level
        current_level_no = 0
        current_level = level_list[current_level_no]

        # Setting up stuff
        player.level = current_level
        enemy.level = current_level
        enemy.player = player

        # Positioning player
        player.rect.x = 340
        player.rect.y = self.screen_height - player.rect.height
        player.rect.x = 340
        player.rect.y = self.screen_height - player.rect.height

        # Sprite list
        active_sprite_list = pygame.sprite.Group()
        active_sprite_list.add(player, head, legs)
        active_sprite_list.add(enemy.bullet_list)
        current_level.enemy_list.add(enemy)

        done = False
        while not done:

            # Mouse position
            mouse_pos = pygame.mouse.get_pos()
            player.mouse = mouse_pos
            head.mouse = mouse_pos

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
                    if event.key == pygame.K_q:
                        # Spawn enemy
                        enemy = Rifleman(player, self)
                        enemy.level = current_level
                        enemy.player = player
                        enemy.rect.x = mouse_pos[0]
                        enemy.rect.y = mouse_pos[1]
                        current_level.enemy_list.add(enemy)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_d and player.change_x > 0:
                        player.stop()

            # UPDATE SPRITES
            active_sprite_list.update()

            # Shooting
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
            if player.dashing:
                if time.time() - player.dash_time >= .25:
                    player.dashing = False
                    player.stop()

            for bullet in level_list[current_level_no].bullet_list:

                # See if it hit a block
                block_hit_list = pygame.sprite.spritecollide(bullet, level_list[current_level_no].block_list,
                                                             False)

                # For each block hit, remove the bullet
                for _ in block_hit_list:
                    level_list[current_level_no].bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)

                # Remove the bullet if it flies up off the screen
                if bullet.rect.x > self.screen_width + 5 or bullet.rect.x < -5:
                    level_list[current_level_no].bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)

            # UPDATE LEVEL
            current_level.update(player)

            # Killing enemies
            for enemy in current_level.enemy_list:
                if not enemy.dead:
                    bullet_hit_list = pygame.sprite.spritecollide(enemy, current_level.bullet_list, True)
                    if len(bullet_hit_list) > 0:
                        enemy.health -= 10
                    if enemy.health <= 0:
                        enemy.die()
                        active_sprite_list.remove(enemy)

            # If the player gets near the right side, shift the world left (-x)
            right_limit = int(self.screen_width * 4 / 5)
            if player.rect.right >= right_limit:
                diff = player.rect.right - right_limit
                player.rect.right = right_limit
                current_level.scroll(-diff)

            # If the player gets near the left side, shift the world right (+x)
            left_limit = int(self.screen_width * 1 / 5)
            if player.rect.left <= left_limit:
                if current_level.level_shift >= 0:
                    current_level.level_shift = 0
                    if player.rect.left <= 0:
                        player.rect.left = 0
                else:
                    diff = left_limit - player.rect.left
                    player.rect.left = left_limit
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

            current_level.draw(self.screen)
            active_sprite_list.draw(self.screen)

            # HEALTH bar
            # Outline
            pygame.draw.rect(self.screen, BLACK,
                             [self.unit_width - 2, self.unit_height / 2 - 2,
                              self.unit_width * 26 + 3, self.unit_height / 2 + 3], 2)
            # Bar
            pygame.draw.rect(self.screen,
                             (255 - int((255 * player.hp / 100) // 1), int((255 * player.hp / 100) // 1), 0),
                             [self.unit_width, self.unit_height / 2,
                              self.unit_width * 13 * player.hp / 50, self.unit_height / 2])
            # ENERGY bar
            # Outline
            pygame.draw.rect(self.screen, BLACK,
                             [self.unit_width - 2, self.unit_height,
                              12 * self.unit_width + 3, self.unit_height / 4 + 5], 2)
            # Bar
            pygame.draw.rect(self.screen, CYAN,
                             [self.unit_width, self.unit_height + 2,
                              self.unit_width * 6 * player.energy / 50, self.unit_height / 4 + 2])

            # ALL CODE TO DRAW SHOULD GO ABOVE

            # Limit to 60 frames per second
            self.clock.tick(60)

            # Update the screen with what we've drawn.
            pygame.display.flip()

        pygame.quit()
