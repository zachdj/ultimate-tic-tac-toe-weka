import random
from models.game.bots.MinimaxBot import MinimaxBot


class RandoMaxBot(MinimaxBot):
    """ Semi-random bot

    This is a minimax bot that scores moves randomly unless the end of the game is seen within a 2-ply lookahead
    """
    def __init__(self, number, max_depth=2, name=None):
        if name is None:
            name = "Rando-Max Bot"
        MinimaxBot.__init__(self, number, max_depth, name=name)
        self.player_type = 'randomax'
        random.seed()

    def compute_score(self, board):
        return random.uniform(-1, 1)
