from ..Player import Player


class Bot(Player):
    """ Abstract base class for UTTT Bots (non-human players)

    Child classes should define an init function that takes the player number and a time_limit
    """
    def __init__(self, number, name=None):
        """

        :param number:  Board.X for player1 or Board.O for player2
        :param name: the name of the
        """
        Player.__init__(self, number, name)
        self.player_type = 'generic bot'

    def is_bot(self):
        return True

    def compute_next_move(self, board, valid_moves):
        """
        Computes the next move for this agent
        :param board: the GlobalBoard object representing the current state of the game
        :param valid_moves: valid moves for the agent
        :return: the Move object recommended for this agent
        """
        raise Exception("You need to override the compute_next_move method in the child class")

    def setup_bot(self, game):
        """
        Game objects will call this function when the bot is initialized.  This allows the bot to perform initial setup
        using game-level variables if needed
        :param game: the game object which this bot is a part of
        :return: None
        """
        raise Exception("You need to override the setup_bot method in the child class")