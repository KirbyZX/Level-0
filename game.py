import time
import pygame

from Animate.player import Player
from Animate.rifleman import Rifleman
from Inanimate.bullet import Bullet
from Level.level_01 import Level_01
from Level.level_02 import Level_02
from constants import *


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

        self.unit_width = self.screen_width / 27
        self.unit_height = self.screen_height / 18

        # Object creation
        self.player = Player(self)
        self.enemy = Rifleman(self.player, self)

        # Personalising
        pygame.display.set_caption("Level Zero")
        pygame.display.set_icon(pygame.transform.scale(self.player.running_frames_r[0], [32, 32]))
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

        # Create all the levels
        self.level_list = [Level_01(self.player, self), Level_02(self.player, self)]

        # Set the current level
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        self.player.level = self.current_level
        self.enemy.level = self.current_level
        self.enemy.player = self.player

        # List creation
        self.active_sprite_list = pygame.sprite.Group()
        self.player.rect.x = 340
        self.player.rect.y = self.screen_height - self.player.rect.height
        self.active_sprite_list.add(self.player)
        self.current_level.enemy_list.add(self.enemy)

        # Loop until the user clicks the close button.
        self.done = False

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def main(self):
        """ Main program """

        while not self.done:

            # Mouse position
            mouse_pos = pygame.mouse.get_pos()
            self.player.mouse = mouse_pos

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.shooting = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.player.shooting = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                    if event.key == pygame.K_h:
                        self.player.hp -= 10
                    if event.key == pygame.K_a:
                        self.player.go_left()
                    if event.key == pygame.K_d:
                        self.player.go_right()
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_e:
                        if self.player.energy >= 25:
                            self.player.dash()
                    if event.key == pygame.K_r:
                        self.player.reverse_gravity = not self.player.reverse_gravity
                    if event.key == pygame.K_q:
                        # Spawn enemy
                        self.enemy = Rifleman(self.player, self)
                        self.enemy.level = self.current_level
                        self.enemy.player = self.player
                        self.enemy.rect.x = mouse_pos[0]
                        self.enemy.rect.y = mouse_pos[1]
                        self.current_level.enemy_list.add(self.enemy)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and self.player.change_x < 0:
                        self.player.stop()
                    if event.key == pygame.K_d and self.player.change_x > 0:
                        self.player.stop()

            # Update the player.
            self.active_sprite_list.add(self.enemy.bullet_list)
            self.active_sprite_list.update()

            # SHOTS FIRED
            if self.player.shooting and time.time() >= self.player.shot_time + self.player.cooldown:
                # Fire a bullet if the user clicks
                bullet = Bullet(mouse_pos)
                # Cooldown calculation code
                self.player.shot_time = time.time()
                # Set the bullet so it is where the player is
                bullet.rect.x = self.player.rect.x + 35
                bullet.rect.y = self.player.rect.y + 10
                bullet.calculate()
                # Add the bullet to the lists
                self.active_sprite_list.add(bullet)
                self.level_list[self.current_level_no].bullet_list.add(bullet)

            # Stopping dashes
            if self.player.dash_list[0]:
                if time.time() - self.player.dash_list[1] >= .25:
                    self.player.dash_list[0] = False
                    self.player.stop()

            for bullet in self.level_list[self.current_level_no].bullet_list:

                # See if it hit a block
                block_hit_list = pygame.sprite.spritecollide(bullet, self.level_list[self.current_level_no].block_list,
                                                             False)

                # For each block hit, remove the bullet
                for _ in block_hit_list:
                    self.level_list[self.current_level_no].bullet_list.remove(bullet)
                    self.active_sprite_list.remove(bullet)

                # Remove the bullet if it flies up off the screen
                if bullet.rect.x > self.screen_width + 5 or bullet.rect.x < -5:
                    self.level_list[self.current_level_no].bullet_list.remove(bullet)
                    self.active_sprite_list.remove(bullet)

            # Update items in the level
            self.current_level.update(self.player)

            # Killing enemies
            for enemy in self.current_level.enemy_list:
                if not enemy.dead:
                    bullet_hit_list = pygame.sprite.spritecollide(enemy, self.current_level.bullet_list, True)
                    if len(bullet_hit_list) > 0:
                        enemy.health -= 10
                    if enemy.health <= 0:
                        enemy.die()
                        self.active_sprite_list.remove(enemy)

            # If the player gets near the right side, shift the world left (-x)
            right_limit = int(self.screen_width * 4 / 5)
            if self.player.rect.right >= right_limit:
                diff = self.player.rect.right - right_limit
                self.player.rect.right = right_limit
                self.current_level.scroll(-diff)

            # If the player gets near the left side, shift the world right (+x)
            left_limit = int(self.screen_width * 1 / 5)
            if self.player.rect.left <= left_limit:
                if self.current_level.level_shift >= 0:
                    self.current_level.level_shift = 0
                    if self.player.rect.left <= 0:
                        self.player.rect.left = 0
                else:
                    diff = left_limit - self.player.rect.left
                    self.player.rect.left = left_limit
                    self.current_level.scroll(diff)

            # If the player gets to the end of the level, go to the next level
            current_position = self.player.rect.x + self.current_level.level_shift
            if current_position < self.current_level.level_limit:
                self.player.rect.x = 120
                if self.current_level_no < len(self.level_list) - 1:
                    self.current_level_no += 1
                    self.current_level = self.level_list[self.current_level_no]
                    self.player.level = self.current_level

            # ALL CODE TO DRAW SHOULD GO BELOW

            self.current_level.draw(self.screen)
            self.active_sprite_list.draw(self.screen)

            # HEALTH bar
            # Outline
            pygame.draw.rect(self.screen, BLACK,
                             [self.unit_width - 2, self.unit_height / 2 - 2,
                              self.unit_width * 24 + 3, self.unit_height / 2 + 3], 2)
            # Bar
            pygame.draw.rect(self.screen,
                             (255 - int((255 * self.player.hp / 100) // 1), int((255 * self.player.hp / 100) // 1), 0),
                             [self.unit_width, self.unit_height / 2,
                              self.unit_width * 12 * self.player.hp / 50, self.unit_height / 2])
            # ENERGY bar
            # Outline
            pygame.draw.rect(self.screen, BLACK,
                             [self.unit_width - 2, self.unit_height,
                              12 * self.unit_width + 3, self.unit_height / 4 + 5]
                             , 2)
            # Bar
            pygame.draw.rect(self.screen, CYAN,
                             [self.unit_width, self.unit_height + 2,
                              self.unit_width * 6 * self.player.energy / 50, self.unit_height / 4 + 2])

            # ALL CODE TO DRAW SHOULD GO ABOVE

            # Limit to 60 frames per second
            self.clock.tick(60)

            # Update the screen with what we've drawn.
            pygame.display.flip()

        pygame.quit()
