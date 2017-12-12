from . import Board
import numpy

class Move(object):
    def __init__(self, player, metarow, metacol, row, col):
        """
        Represents a move made at the specified metarow, metacol, row, and col
        :param player: the player number making the move.  Should be Board.X or Board.O
        :param metarow: the row number of the meta-cell where the move is located
        :param metacol: the col number of the meta-cell where the move is located
        :param row: the row number of the microboard cell where the move is located
        :param col: the col number of the microboard cell where the move is located
        """
        # check input validity
        if player not in [Board.X, Board.O]:
            raise Exception("Tried to initialize move for player number %s" % player)
        if (numpy.array([metarow, metacol, row, col]) > 2).any() or (numpy.array([metarow, metacol, row, col]) < 0).any():
            raise Exception("Move index out of bounds")

        self.player = player
        self.metarow = metarow
        self.metacol = metacol
        self.row = row
        self.col = col

        # abs_row, abs_col represent the location of the move on a 9x9 grid
        self.abs_row = metarow*3 + row
        self.abs_col = metacol*3 + col

    def __str__(self):
        return "Player %s made a move at (%s, %s, %s, %s)" % (self.player, self.metarow, self.metacol, self.row, self.col)

    def __eq__(self, other):
        return self.player == other.player and self.metarow == other.metarow and self.metacol == other.metacol \
            and self.row == other.row and self.col == other.col

    def __ne__(self, other):
        return not self.__eq__(other)
