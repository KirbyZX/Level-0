from Level.level import Level
from Level.block import Block
from Level.block_moving import MovingBlock
from Level.platform import Platform


class Level_01(Level):
    """
    Definition for level 1.
    """

    def __init__(self, player):
        """ Create level 1. """

        # Call parent constructor
        Level.__init__(self, player)

        self.level_limit = -1000

        # Array with width, height, x, and y of platforms
        level = [
            [500, 600, "Platform"],
            [800, 500, "Block"],
            [1000, 400, "Block"],
            [1120, 280, "Block"],
                ]

        # Go through the array above and add platforms
        for platform in level:
            if platform[2] == "Block":
                block = Block()
            elif platform[2] == "Platform":
                block = Platform()
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            block.player = self.player
            self.block_list.add(block)

        # Add a moving block
        block = MovingBlock()
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.block_list.add(block)
