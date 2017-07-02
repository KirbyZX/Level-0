from menu import Menu
from button import Button


class StartMenu(Menu):
    """
    Defining the start menu.
    """

    def __init__(self, game):
        """ Creating the start menu. """

        Menu.__init__(self, game)

        buttons = [
            [500, 500, "Hi"],
            [1000, 500, "Hello"]
                  ]

        for button in buttons:
            b = Button(button[2], game)
            b.rect.x = button[0]
            b.rect.y = button[1]
            b.text = button[2]
            b.text.rect.x = button[0]
            b.text.rect.y = button[1]
            self.button_list.add(b)
            self.text_list.add(b.text)
