from Level.level import Level
from Level.block import Block
from Level.block_moving import MovingBlock


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
            [450, 570],
            [850, 420],
            [1000, 520],
            [1120, 280],
                ]

        # Go through the array above and add platforms
        for platform in level:
            block = Block()
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            block.player = self.player
            self.block_list.add(block)

        # Add a custom moving block
        block = MovingBlock()
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.block_list.add(block)
