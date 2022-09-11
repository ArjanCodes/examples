import unittest
from logic import ChessLogic
from pieces import *


class TestingPieces(unittest.TestCase):
    def setUp(self):
        self.game = ChessLogic()
        self.board = self.game.board

    def testQueenMoves(self):
        self.game.populate_with_fen("rnb1kbnr/pppppppp/8/4P1q1/8/8/PPPPPPPP/RNBQKBNR")
        correctMoves = set(
            [
                (5, 4),
                (4, 5),
                (3, 6),
                (7, 4),
                (7, 2),
                (5, 2),
                (7, 3),
                (5, 3),
                (4, 3),
                (6, 4),
                (6, 5),
                (6, 6),
                (6, 2),
            ]
        )
        queenMoves = self.board[3][6].get_moves(self.board)
        self.assertTrue(len(queenMoves) == len(correctMoves))
        for x in queenMoves:
            self.assertTrue(x in correctMoves)

    def testBishopMoves(self):
        self.game.populate_with_fen("rn1qkbnr/pppppppp/8/4b3/8/8/PPPPPPPP/RNBQKBNR")
        correctMoves = set(
            [(3, 2), (5, 2), (3, 4), (2, 5), (1, 6), (5, 4), (6, 5), (7, 6)]
        )
        bishopMoves = self.board[3][4].get_moves(self.board)
        self.assertTrue(len(bishopMoves) == len(correctMoves))
        for x in bishopMoves:
            self.assertTrue(x in correctMoves)

    def testKnightMoves(self):
        self.game.populate_with_fen("r1bqkbnr/pppppppp/8/8/4n3/8/PPPPPPPP/RNBQKBNR")
        correctMoves = set(
            [(2, 5), (2, 3), (3, 6), (3, 2), (5, 6), (5, 2), (6, 5), (6, 3)]
        )
        knightMoves = self.board[4][4].get_moves(self.board)
        self.assertTrue(len(knightMoves) == len(correctMoves))
        for x in knightMoves:
            self.assertTrue(x in correctMoves)


class TestingChecks(unittest.TestCase):
    def setUp(self):
        self.game = ChessLogic()
        self.board = self.game.board

    def testCheck(self):
        self.game.populate_with_fen("rnbqkbnr/ppppp1pp/5p2/6pQ/8/4P3/PPPP1PPP/RNB1KBNR")
        self.game.player_turn = 1
        self.assertTrue(self.game.check_for_check())
        self.assertFalse(self.game.check_for_mate())

    def testCheckMate(self):
        self.game.populate_with_fen("rnb1kbnr/pppp1ppp/8/8/6Pq/5P2/PPPPP11P/RNBQKBNR")
        self.assertTrue(self.game.check_for_check())
        self.assertTrue(self.game.check_for_mate())


if __name__ == "__main__":
    unittest.main()
