import unittest

from . import Move, Board, LocalBoard, GlobalBoard, Player, Game


class MoveUnitTest(unittest.TestCase):
    def setUp(self):
        self.move1 = Move(Board.X, 0, 0, 0, 0)
        self.move2 = Move(Board.X, 1, 0, 0, 0)
        self.move3 = Move(Board.X, 2, 1, 2, 1)
        self.move4 = Move(Board.X, 0, 2, 1, 2)

    def test_abs_row(self):
        self.assertEqual(self.move1.abs_row, 0)
        self.assertEqual(self.move2.abs_row, 3)
        self.assertEqual(self.move3.abs_row, 8)
        self.assertEqual(self.move4.abs_row, 1)

    def test_abs_col(self):
        self.assertEqual(self.move1.abs_col, 0)
        self.assertEqual(self.move2.abs_col, 0)
        self.assertEqual(self.move3.abs_col, 4)
        self.assertEqual(self.move4.abs_col, 8)

    def test_out_of_bounds_input(self):
        with self.assertRaises(Exception):
            bad_move = Move(55, 0, 0, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, 3, 0, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, 3, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, 0, 0, 3, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, 0, 0, 3)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, -3, 0, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, -3, 0, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.X, 0, 0, -3, 0)
        with self.assertRaises(Exception):
            bad_move = Move(Board.O, 0, 0, 0, -3)


class LocalBoardUnitTest(unittest.TestCase):
    def test_moves(self):
        board1 = LocalBoard()
        move1 = Move(Board.X, 0, 0, 0, 0)
        board1.make_move(move1)
        self.assertEqual(board1.check_cell(0, 0), Board.X)

        with self.assertRaises(Exception):
            move2 = Move(Board.O, 0, 0, 0, 0)
            board1.make_move(move2)
        with self.assertRaises(Exception):
            move2 = Move(Board.O, 0, 1, 0, 0)
            board1.make_move(move2)

        move2 = Move(Board.O, 0, 1, 1, 0)
        board1.make_move(move2)
        self.assertEqual(board1.check_cell(1, 0), Board.O)

        self.assertFalse(board1.board_completed)
        self.assertEqual(board1.winner, Board.EMPTY)

    def test_game_over(self):
        # win a board and check the winner
        move_seq = [
            Move(Board.X, 0, 0, 0, 0),
            Move(Board.X, 0, 0, 1, 1),
            Move(Board.X, 0, 0, 2, 2)
        ]
        board = LocalBoard()
        for move in move_seq:
            board.make_move(move)
        self.assertTrue(board.board_completed)
        self.assertEqual(board.winner, Board.X)

        # tie a board and check for cat
        move_seq = [
            Move(Board.X, 0, 0, 0, 0),
            Move(Board.O, 0, 0, 0, 1),
            Move(Board.X, 0, 0, 0, 2),
            Move(Board.O, 0, 0, 1, 0),
            Move(Board.O, 0, 0, 1, 1),
            Move(Board.X, 0, 0, 1, 2),
            Move(Board.X, 0, 0, 2, 0),
            Move(Board.X, 0, 0, 2, 1),
            Move(Board.O, 0, 0, 2, 2)
        ]
        board = LocalBoard()
        for move in move_seq:
            board.make_move(move)
        self.assertTrue(board.board_completed)
        self.assertTrue(board.cats_game)
        self.assertEqual(board.winner, Board.EMPTY)


class GlobalBoardUnitTest(unittest.TestCase):
    def test_moves(self):
        board = GlobalBoard()
        moves = [
            Move(Board.X, 0, 0, 0, 0),
            Move(Board.X, 0, 0, 1, 1),
            Move(Board.X, 0, 0, 2, 2),
            Move(Board.X, 1, 1, 0, 0),
            Move(Board.X, 1, 1, 1, 1),
            Move(Board.X, 1, 1, 2, 2),
            Move(Board.X, 2, 2, 0, 0),
            Move(Board.X, 2, 2, 1, 1),
            Move(Board.X, 2, 2, 2, 2),
        ]

        for move in moves:
            board.make_move(move)

        self.assertTrue(board.board_completed)
        self.assertEqual(board.winner, Board.X)

        with self.assertRaises(Exception):
            board.make_move(Move(Board.O, 2, 2, 0, 0))

    def test_get_valid_moves(self):
        board = GlobalBoard()
        move1 = Move(Board.X, 1, 1, 1, 1)
        board.make_move(move1)
        valid_moves = board.get_valid_moves(move1)
        self.assertEqual(len(valid_moves), 8)
        self.assertEqual(valid_moves[0].player, Board.O)

        move2 = Move(Board.X, 1, 1, 0, 0)
        move3 = Move(Board.X, 1, 1, 2, 2)
        board.make_move(move2)
        board.make_move(move3)

        valid_moves = board.get_valid_moves(move3)  # test sending opponent to an empty board
        self.assertEqual(len(valid_moves), 9)

        valid_moves = board.get_valid_moves(move1)  # test sending opponent to a board that has been won
        self.assertEqual(len(valid_moves), 72)


class PlayerUnitTest(unittest.TestCase):
    def test_init(self):
        player1 = Player(Board.X)
        self.assertEqual(player1.number, Board.X)
        self.assertEqual(player1.name, "Player %s" % Board.X)

        player2 = Player(Board.O, "Fred Finn")
        self.assertEqual(player2.name, "Fred Finn")

        with self.assertRaises(Exception):
            player3 = Player(Board.EMPTY)


class GameUnitTest(unittest.TestCase):
    def test_tied_game(self):
        moves = [
            Move(Board.X, 1, 0, 2, 2),
            Move(Board.O, 2, 2, 1, 1),
            Move(Board.X, 1, 1, 2, 2),
            Move(Board.O, 2, 2, 2, 2),
            Move(Board.X, 2, 2, 2, 0),
            Move(Board.O, 2, 0, 1, 2),
            Move(Board.X, 1, 2, 0, 1),
            Move(Board.O, 0, 1, 0, 0),
            Move(Board.X, 0, 0, 0, 0),
            Move(Board.O, 0, 0, 0, 1),
            Move(Board.X, 0, 1, 1, 0),
            Move(Board.O, 1, 0, 2, 1),
            Move(Board.X, 2, 1, 1, 1),
            Move(Board.O, 1, 1, 1, 0),
            Move(Board.X, 1, 0, 2, 0),
            Move(Board.O, 2, 0, 2, 2),
            Move(Board.X, 2, 2, 1, 0),
            Move(Board.O, 1, 0, 0, 2),
            Move(Board.X, 0, 2, 2, 1),
            Move(Board.O, 2, 1, 0, 1),
            Move(Board.X, 0, 1, 2, 2),
            Move(Board.O, 2, 2, 0, 1),
            Move(Board.X, 0, 1, 2, 0),
            Move(Board.O, 2, 0, 0, 0),
            Move(Board.X, 0, 0, 1, 1),
            Move(Board.O, 1, 1, 2, 1),
            Move(Board.X, 2, 1, 2, 1),
            Move(Board.O, 2, 1, 0, 0),
            Move(Board.X, 0, 0, 1, 0),
            Move(Board.O, 1, 0, 0, 0),
            Move(Board.X, 0, 0, 2, 0),
            Move(Board.O, 2, 0, 0, 1),
            Move(Board.X, 0, 1, 2, 1),
            Move(Board.O, 2, 1, 1, 0),
            Move(Board.X, 1, 0, 1, 2),
            Move(Board.O, 1, 2, 1, 2),
            Move(Board.X, 1, 2, 0, 0),
            Move(Board.O, 1, 2, 1, 0),
            Move(Board.X, 1, 0, 1, 1),
            Move(Board.O, 1, 1, 0, 1),
            Move(Board.X, 2, 0, 1, 1),
            Move(Board.O, 1, 1, 1, 2),
            Move(Board.X, 1, 2, 0, 2),
            Move(Board.O, 0, 2, 1, 1),
            Move(Board.X, 1, 1, 1, 1),
            Move(Board.O, 1, 1, 2, 0),
            Move(Board.X, 2, 0, 0, 2),
            Move(Board.O, 0, 2, 1, 2),
            Move(Board.X, 2, 1, 0, 2),
            Move(Board.O, 0, 2, 1, 0),
            Move(Board.X, 1, 0, 1, 0),
            Move(Board.O, 2, 1, 2, 2),
            Move(Board.X, 2, 2, 0, 0),
            Move(Board.O, 2, 0, 2, 0),
            Move(Board.X, 2, 0, 2, 1),
            Move(Board.O, 2, 1, 1, 2),
            Move(Board.X, 2, 0, 1, 0),
            Move(Board.O, 1, 1, 0, 0),
            Move(Board.X, 2, 1, 2, 0),
        ]
        p1 = Player(Board.X)
        p2 = Player(Board.O)
        game = Game(p1, p2)
        for move in moves:
            game.make_move(move)

        self.assertTrue(game.is_game_over())
        self.assertEqual(game.get_winner(), Board.EMPTY)

if __name__ == '__main__':
    unittest.main()