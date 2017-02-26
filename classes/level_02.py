from classes.platform import Platform
from classes.platform_moving import MovingPlatform
from classes.level import Level


class Level_02(Level):
    """
    Definition for level 2.
    """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with width, height, x, and y of platforms
        level = [
            [210, 30, 450, 570],
            [210, 30, 850, 420],
            [210, 30, 1000, 520],
            [210, 30, 1120, 280],
                ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
