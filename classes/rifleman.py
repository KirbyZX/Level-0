from classes.enemy import Enemy


class Rifleman(Enemy):
    """
    Child class of Enemy to represent
    a basic rifleman.
    """

    def __init__(self, player):
        """ Constructing the enemy """

        # Parent constructor
        Enemy.__init__(self, player)

        self.hp = 0
        self.attacks = []





