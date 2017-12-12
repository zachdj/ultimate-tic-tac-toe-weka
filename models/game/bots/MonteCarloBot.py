import random, numpy, timeit
from .TimeLimitedBot import TimeLimitedBot
from ..Board import Board
from services import ApplicationStatusService

# TODO: Save MCTS tree and reuse nodes as moves are chosen
"""
    Some ideas on this implementation:
    (Written at 3:04 am on a Wednesday so take these with a grain or two of salt)
    The bot is currently setup to minimize the chances of player 2s success.  This may be causing it to be content with ties
    Also, the bot assumes the other player is completely random.  This seems to give the bot a predilection towards choosing moves with a high branching factor
    
    
"""


class MonteCarloBot(TimeLimitedBot):
    """
    This bot performs a Monte Carlo Tree Search to find a move
    """
    def __init__(self, player, time_limit=10):
        """
        Creates a new Monte Carlo Tree Search Bot
        :param player: the player that this bot will play as.  Either Board.X or Board.O
        :param time_limit: The maximum computation time, in seconds
        """
        TimeLimitedBot.__init__(self, player, time_limit, "MCTS Bot")
        self.time_limit = time_limit
        self.player_type = 'mcts bot'
        self.game = None  # we'll set this in the setup function

        random.seed()

    def setup_bot(self, game):
        self.game = game

    def compute_next_move(self, board, valid_moves):
        begin = timeit.default_timer()
        last_move = None
        if len(self.game.moves) > 0:
            last_move = self.game.moves[-1]
        root_node = _Node(self.game.board, last_move)
        while (timeit.default_timer() - begin) < self.time_limit and not ApplicationStatusService.terminated:
            selected_node = root_node.select_node()
            expanded_node = selected_node.expand_node()
            expanded_node.do_playout()

        best_score = -100
        selected_move = None
        for child in root_node.children:
            # check if the move wins the game for this player
            dummy_board = self.game.board.clone()
            dummy_board.make_move(child.last_move)
            if dummy_board.winner == self.number:
                selected_move = child.last_move
                break

            if child.games_recorded == 0:  # a move with no recorded stats is treated like a draw
                score = 0
            else:
                total = child.games_recorded
                wins = child.wins_recorded
                ties = child.ties_recorded
                losses = total - wins - ties

                score = -(wins - losses) / total  # reverse the sign of the score since the child node is the opponent
            if score > best_score:
                best_score = score
                selected_move = child.last_move
        return selected_move


# private class for nodes in the Monte Carlo game tree
class _Node(object):
    def __init__(self, board, last_move, parent=None):
        # setup variables needed to compute child nodes and update the nodes value
        self.wins_recorded = 0
        self.ties_recorded = 0
        self.games_recorded = 0
        self.board = board
        self.last_move = last_move
        self.player = Board.X
        if last_move is not None and last_move.player == Board.X:
            self.player = Board.O
        self.parent = parent
        self.is_leaf = True

        self.children = []

    def compute_uct_score(self, exploration_param=1.41421356):
        """
        Computes the UCT1 value for this node
        UCT1 = w / n  + c * sqrt( ln(N) / n)
        where w = number of wins recorded for this node, n = number of playouts recorded for this node,
        c = tunable exploration parameter ( default sqrt(2) ), and N = total playouts recorded for all nodes
        :param exploration_param: the parameter c determining the strength of the exploration component of UCT1
        :return: the UCT1 value of this node
        """

        # if no playouts have been recorded, then this node gets the max value
        if self.games_recorded == 0:
            return float('inf')

        # otherwise compute the score as normal
        # follow the path back to the root node to get total number of playouts
        root = self
        while root.parent is not None:
            root = root.parent

        total_playouts = root.games_recorded
        return (self.wins_recorded / self.games_recorded) + exploration_param * numpy.sqrt( numpy.log(total_playouts) / self.games_recorded)

    def select_node(self):
        """
        Selection phase of the MCTS algorithm
        If the node is a leaf, then a random child is selected
        Otherwise, successive child nodes are selected down to a leaf using UCT1 scores

        :return: the selected node
        """
        if self.is_leaf:  # a node will be a leaf if it's a terminal state or if it has no expanded children
            selection = self
        else:
            max_uct = -1
            next_node_in_tree = None
            for child in self.children:
                child_uct = child.compute_uct_score()
                if child_uct > max_uct:
                    next_node_in_tree = child
                    max_uct = child_uct
            selection = next_node_in_tree.select_node()  # recursively descends to a leaf node

        return selection

    def expand_node(self):
        """
        Expansion phase of the MCTS algorithm.
        If this node is terminal, then just return thiss node
        Else If this node has at least one playout, create child nodes and randomly select one.
        Otherwise, just return the current node
        :return: the node selected for playout
        """
        if self.board.board_completed:
            return self
        elif self.games_recorded == 0:
            return self
        else:
            self.is_leaf = False
            # generate children of this node
            valid_moves = self.board.get_valid_moves(self.last_move)
            for move in valid_moves:
                cloned_board = self.board.clone()
                cloned_board.make_move(move)
                child_node = _Node(cloned_board, move, parent=self)
                self.children.append(child_node)

            # select one for playout
            return random.choice(self.children)

    def do_playout(self):
        """
        Plays out a game from this node by randomly selecting moves until the board is completed
        :return: None
        """
        board = self.board.clone()
        last_move = self.last_move
        while not board.board_completed:
            valid_moves = board.get_valid_moves(last_move)
            selected_move = random.choice(valid_moves)
            board.make_move(selected_move)
            last_move = selected_move

        winner = board.winner
        self.backpropogate(winner)

    def backpropogate(self, winner):
        """
        Propogates the result of a playout upwards to the root node
        :return: None
        """
        parent = self
        while parent is not None:
            parent.games_recorded += 1
            if parent.player == winner:
                parent.wins_recorded += 1
            elif winner == Board.EMPTY or winner == Board.CAT:
                parent.ties_recorded += 1
            parent = parent.parent
