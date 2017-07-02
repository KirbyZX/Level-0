import pygame

from constants import *


class Menu:
    """
    Super-class to define a menu with buttons etc.
    Create a child class for each menu with menu-specific info.
    """

    def __init__(self, game):
        """ Constructor """

        self.button_list = pygame.sprite.Group()
        self.text_list = pygame.sprite.Group()
        self.game = game
        self.alive = True

    def draw(self, screen):

        screen.fill(WHITE)

        self.button_list.draw(screen)
        self.text_list.draw(screen)

    def check(self):
        """ Interaction of buttons """

        while self.alive:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    for button in self.button_list:
                        if button.rect.x < mouse_pos[0] < button.rect.x + button.width and button.rect.y < mouse_pos[1] < button.rect.y + button.height:
                            return button

