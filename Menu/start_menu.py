from Menu.button import Button
from Menu.menu import Menu
from Menu.text import Text
from constants import *


class StartMenu(Menu):
    """
    Defining the start menu.
    """

    def __init__(self, game):
        """ Creating the start menu. """

        Menu.__init__(self, game)

        buttons = [
            # x,  y, w, h, text
            [12, 6, 4, 1, "Start"],
            [12, 7.5, 4, 1, "Exit"]
        ]

        for button in buttons:
            b = Button(button[2], button[3], button[4], game)
            b.rect.x = button[0] * game.unit_width
            b.rect.y = button[1] * game.unit_height
            self.button_list.add(b)

        texts = [
            # text,    size, colour, cx, cy
            ["Start",   70,  BLACK,  14, 6.5],
            ["Exit",    70,  BLACK,  14, 8],
            ["Level 0", 200, WHITE,  14, 3]
        ]

        for text in texts:
            t = Text(text[0], text[1], text[2], game)
            t.rect.centerx = text[3] * game.unit_width
            t.rect.centery = text[4] * game.unit_width
            self.text_list.add(t)
