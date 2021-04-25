from abc import ABC, abstractmethod
from hand import Hand

class Rule(ABC):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def points(self, hand: Hand):
        pass

    @abstractmethod
    def is_valid(self, hand: Hand):
        pass

class Aces(Rule):

    def name(self):
        return "Aces"

    def points(self, hand: Hand):
        return hand.count(1) * 1

    def is_valid(self, hand: Hand):
        return True

class Twos(Rule):

    def name(self):
        return "Twos"

    def points(self, hand: Hand):
        return hand.count(2) * 2

    def is_valid(self, hand: Hand):
        return True


class Rules:

    def __init__(self):
        self.rules_map = {
            1: self.aces,
            2: self.twos,
            3: self.threes,
            4: self.fours,
            5: self.fives,
            6: self.sixes,
            7: self.three_of_a_kind,
            8: self.four_of_a_kind,
            9: self.full_house,
            10: self.small_straight,
            11: self.large_straight,
            12: self.yahtzee,
            13: self.chance,
        }

    def aces(self, hand):
        return hand.count(1) * 1

    def twos(self, hand):
        return hand.count(2) * 2

    def threes(self, hand):
        return hand.count(3) * 3

    def fours(self, hand):
        return hand.count(4) * 4

    def fives(self, hand):
        return hand.count(5) * 5

    def sixes(self, hand):
        return hand.count(6) * 6

    def three_of_a_kind(self, hand):
        for i in range(6):
            if hand.count(i + 1) >= 3:
                return hand.sum()
        return 0

    def four_of_a_kind(self, hand):
        for i in range(6):
            if hand.count(i + 1) >= 4:
                return hand.sum()
        return 0

    def full_house(self, hand):
        counts = [hand.count(i + 1) for i in range(6)]
        print(counts)
        if 2 in counts and 3 in counts:
            return 25
        else:
            return 0

    def small_straight(self, hand):
        l = list(set(hand.get_hand()))
        # sum of consecutive n numbers 1...n = n * (n+1) / 2 
        consecutive_sum = max(l) * (max(l) + 1) / 2 - ((min(l) - 1) * (min(l))/2)
        if len(l) >= 4 and sum(l) == consecutive_sum:
            return 30
        else:
            return 0

    def large_straight(self, hand):
        l = list(set(hand.get_hand()))
        # sum of consecutive n numbers 1...n = n * (n+1) / 2 
        consecutive_sum = max(l) * (max(l) + 1) / 2 - ((min(l) - 1) * (min(l))/2)
        if len(l) >= 5 and sum(l) == consecutive_sum:
            return 40
        else:
            return 0

    def yahtzee(self, hand):
        if len(set(hand.get_hand())) == 1:
            return 50
        return 0

    def chance(self, hand):
        return hand.sum()