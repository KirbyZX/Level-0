from Level.level import Level
from Level.block import Block
from Level.block_moving import MovingBlock
from Level.platform import Platform


class Level_01(Level):
    """
    Definition for level 1.
    """

    def __init__(self, player, game):
        """ Create level 1. """

        # Call parent constructor
        Level.__init__(self, player, game)

        self.level_limit = -1000

        # Array with x, y and type of block
        level = [
            [500, 500, "platform"],
            [800, 1000, "block"],
            [1000, 400, "block"],
            [1120, 280, "block"],
                ]

        # Go through the array above and add platforms
        for platform in level:
            if platform[2] == "block":
                block = Block(game)
            elif platform[2] == "platform":
                block = Platform()
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            block.player = self.player
            self.block_list.add(block)

        # Add a moving block
        block = MovingBlock(game)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.block_list.add(block)
