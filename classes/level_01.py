from classes.platform import Platform
from classes.platform_moving import MovingPlatform
from classes.level import Level


class Level_01(Level):
    """
    Definition for level 1.
    """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with width, height, x, and y of platforms
        level = [
            [210, 70, 500, 600],
            [210, 70, 800, 500],
            [210, 70, 1000, 400],
            [210, 70, 1120, 280],
                ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        # Add a moving platform
        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
