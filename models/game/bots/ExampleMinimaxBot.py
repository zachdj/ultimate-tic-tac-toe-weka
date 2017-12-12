import numpy
from models.game.bots.MinimaxBot import MinimaxBot
from models.data.BoardDataModel import BoardDataModel


class ExampleMinimaxBot(MinimaxBot):
    """ Example child class of MinimaxBot

    This bot shows how to override the scoring method.  In this particular example, the scoring method just sums up
    the cells of the board and divides by a regularizing constant.
    The scoring function doesn't make any sense.  It just shows how to compute a score if you have a vector of weights
    """
    def __init__(self, number, max_depth=5, name=None):
        """
        The init method should follow this pattern.  Just change the name of the bot.

        :param number:  Board.X for player1 or Board.O for player2
        :param max_depth:  The maximum depth of the lookahead
        :param name: A descriptive name for the Bot
        """
        if name is None:
            name = "Example Minimax"
        MinimaxBot.__init__(self, number, max_depth, name=name)
        self.player_type = 'example minimax'

    def compute_score(self, board):
        data_model = BoardDataModel(board)
        representation_vector = data_model.representation
        next_player = data_model.next_player
        representation_vector.append(next_player)  # representation is now like a row of the board table.  81 cells and the next_player

        weights = numpy.ones(82) * (1/82)
        sum = weights.dot(representation_vector)  # multiplies the weights times the representation vector and sums over each product
        return sum
