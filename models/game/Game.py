from .GlobalBoard import GlobalBoard
from .bots.Bot import Bot


class Game(object):
    def __init__(self, player1, player2):
        """
        Game objects represent a game played between two opponents.  Zero, one, or both of the opponents can be bots
        :param player1: Player or Bot object corresponding to the 'X' player
        :param player2: Player or Bot object corresponding to the 'O' player
        """
        self.board = GlobalBoard()
        self.player1 = player1
        self.player2 = player2
        self.active_player = player1  # the player who moves next is the active player.  Player 1 always goes first
        self.bot_game = isinstance(player1, Bot) and isinstance(player2, Bot)
        self.moves = []
        if isinstance(player1, Bot):
            self.player1.setup_bot(self)

        if isinstance(player2, Bot):
            self.player2.setup_bot(self)

    def make_move(self, move):
        """
        Applies the given move to this game.  Raises an exception if the move is taken out-of-turn
        :param move: the Move object to make
        :return: None
        """
        if move.player != self.active_player.get_player_symbol():
            raise Exception("Error making move: It is not player %s's turn" % move.player)

        self.board.make_move(move)
        self.moves.append(move)
        if move.player == self.player1.get_player_symbol():
            self.active_player = self.player2
        else:
            self.active_player = self.player1

    def get_valid_moves(self):
        """ Gets the valid moves for the current player.  Wrapper around the get_valid_moves method of GlobalBoard
        :return: list of Move objects which are valid for the current board state
        """
        if len(self.moves) > 0:
            return self.board.get_valid_moves(self.moves[-1])
        else:
            return self.board.get_possible_moves(self.active_player.get_player_symbol())

    def is_game_over(self):
        return self.board.board_completed

    def get_winner(self):
        if self.is_game_over():
            return self.board.winner
        else:
            raise Exception("Cannot get the winner of a game which has not been completed")

    def finish_game(self):
        """ For bot games (where both players are bots) attempts to finish the game by continually polling the bots
        for moves until the game has ended.
        :return: the player number of the winner of the game
        """
        if not self.bot_game:
            raise Exception("Games can only be finished automatically if both players are bots")

        while not self.is_game_over():
            self._take_step()

        return self.get_winner()

    def _take_step(self):
        """ For bot games (where both players are bots), polls the active player for a move and executes the move
        :return: the selected Move
        """
        next_move = self.active_player.compute_next_move(self.board, self.get_valid_moves())
        self.make_move(next_move)
        return next_move

