import unittest

from yahtzee import *


class HandTestCase(unittest.TestCase):

    def test_hand_number_of_dice(self):
        hand = Hand(15, 6)
        self.assertEqual(len(hand.hand), 15)

    def test_hand_sides_per_die(self):
        hand = Hand(5, 18)
        for i in hand.hand:
            self.assertEqual(i.sides, 18)


class RulesTestCase(unittest.TestCase):

    def test_aces(self):
        hand = Hand()
        for i in hand.hand:
            i._Die__face = 1
        self.assertEqual(Rules().aces(hand), 5)

    def test_three_of_a_kind(self):
        hand = Hand()
        for i in range(3):
            hand.hand[i]._Die__face = 1
        for i in range(3, 5):
            hand.hand[i]._Die__face = 2
        self.assertEqual(Rules().three_of_a_kind(hand), 7)

    def test_four_of_a_kind(self):
        hand = Hand()
        for i in range(4):
            hand.hand[i]._Die__face = 1
        for i in range(4, 5):
            hand.hand[i]._Die__face = 2
        self.assertEqual(Rules().four_of_a_kind(hand), 6)

    def test_full_house(self):
        hand = Hand()
        for i in range(1):
            hand.hand[i]._Die__face = 2
        for i in range(1, 3):
            hand.hand[i]._Die__face = 2
        for i in range(3, 5):
            hand.hand[i]._Die__face = 3
        self.assertEqual(Rules().full_house(hand), 25)

    def test_small_straight(self):
        hand = Hand()
        hand.hand[0]._Die__face = 4
        hand.hand[1]._Die__face = 3
        hand.hand[2]._Die__face = 5
        hand.hand[3]._Die__face = 2
        hand.hand[4]._Die__face = 5
        self.assertEqual(Rules().small_straight(hand), 30)

    def test_large_straight(self):
        hand = Hand()
        hand.hand[0]._Die__face = 4
        hand.hand[1]._Die__face = 3
        hand.hand[2]._Die__face = 5
        hand.hand[3]._Die__face = 2
        hand.hand[4]._Die__face = 1
        self.assertEqual(Rules().large_straight(hand), 40)

    def test_yahtzee(self):
        hand = Hand()
        for i in hand.hand:
            i._Die__face = 3
        self.assertEqual(Rules().yahtzee(hand), 50)

    def test_chance(self):
        hand = Hand()
        for i in range(5):
            hand.hand[i]._Die__face = i + 1
        self.assertEqual(Rules().chance(hand), 15)

print(list(range(1, 5)))
if __name__ == '__main__':
    unittest.main()
