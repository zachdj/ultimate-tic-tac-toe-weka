from . import Board


class Player(object):
    """ Represents a human player
    """

    def __init__(self, number, name=None):
        self.player_type = 'human'
        if number != Board.X and number != Board.O:
            raise Exception("Tried to initialize player with invalid player symbol.")
        self.number = number
        if name:
            self.name = name
        else:
            self.name = "Player %s" % number

    def is_bot(self):
        return False

    def get_player_symbol(self):
        """ Gets the symbol ('X' or 'O') for the given player
        :return: Board.X if player is the 'X' player;  Board.O if the player is the 'O' player
        """
        return self.number
