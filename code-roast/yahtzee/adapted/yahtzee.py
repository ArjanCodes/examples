#!/usr/bin/env python

"""Yahtzee, the board game!

This python program will simulate a game of Yahtzee
"""

import sys
import os
import random
import re
from hand import Die, Hand
from rules import *

class ScoreBoard(object):

    # TODO: Everything
    def __init__(self):
        self.scoreboard_rows = [
            Aces(),
            Twos(),
            Threes(),
            Fours(),
            Fives(),
            Sixes(),
            ThreeOfAKind(),
            FourOfAKind(),
            FullHouse(),
            SmallStraight(),
            LargeStraight(),
            Yahtzee(),
            Chance(),
        ]
        # Once again, prevent cheating with private variables
        self.__scoreboard_points = [0] * len(self.scoreboard_rows)

    def assign_points(self, row: int, hand: Hand):
        if row < 0 or row >= len(self.scoreboard_rows):
            raise IndexError("Bad row index")
        elif self.__scoreboard_points[row] > 0:
            raise Exception("ScoreBoard already saved!")
        else:
            rule = self.scoreboard_rows[row]
            points = rule.points(hand)
            print(f"Adding {points} points to {rule.name()}")
            self.__scoreboard_points[row] = points

    def get_scoreboard_points(self):
        return self.__scoreboard_points

    def show_scoreboard_rows(self):
        for idx, rule in enumerate(self.scoreboard_rows):
            print(f"{idx + 1}. {rule.name()}")

    def show_scoreboard_points(self, hand: Hand = None):
        print("\nSCOREBOARD")
        print("===================================")
        for idx, rule in enumerate(self.scoreboard_rows):
            points = self.__scoreboard_points[idx]
            if hand is not None and points == 0 and rule.points(hand) > 0:
                print(f"{idx + 1}. {rule.name()}: +{rule.points(hand)} points ***")
            else:
                print(f"{idx + 1}. {rule.name()}: {[points]} points")
        print("===================================")

    def select_scoring(self, hand: Hand):
        self.show_scoreboard_points(hand)
        while True:
            scoreboard_row = input("Choose which scoring to use: ")
            try:
                scoreboard_row_int = int(re.sub('[^0-9,]', '', scoreboard_row))
                if scoreboard_row_int < 1 or scoreboard_row_int > len(self.scoreboard_rows):
                    print("Please select an existing scoring rule.")
                else:
                    return scoreboard_row_int - 1
            except ValueError:
                print("You entered something other than a number. Please try again.")

def choose_dice_reroll(hand):
    while True:
        try:
            reroll = input("\nChoose which dice to re-roll "
                            "(comma-separated or 'all'), or 0 to continue: ")

            if reroll.lower() == "all":
                return hand.all_dice()
            else:
                # Perform some clean-up of input
                reroll = reroll.replace(" ", "")  # Remove spaces
                reroll = re.sub('[^0-9,]', '', reroll)  # Remove non-numerals
                reroll = reroll.split(",")  # Turn string into list
                reroll = list(map(int, reroll))  # Turn strings in list to int
            
            if not reroll or 0 in reroll:
                return []
            else:
                return reroll

        except ValueError:
            print("You entered something other than a number.")
            print("Please try again")
        except IndexError as i:
            print(i)

def Main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
YAHTZEE

Welcome to the game. To begin, simply press [Enter]
and follow the instructions on the screen.

To exit, press [Ctrl+C]
""")

    # Begin by instantiating the hand and scoreboard
    hand = Hand()
    scoreboard = ScoreBoard()
    

    # We keep going until the scoreboard is full
    for i in range(len(scoreboard.scoreboard_rows)):
        rolls = 0
        selected_dice = hand.all_dice()
        while True:
            
            # roll the dice
            print("\nRolling dice...")
            hand.roll(selected_dice)
            print(hand)
            rolls += 1

            # if we reached the maximum number of rolls, we're done
            if rolls >= 3:
                break

            # choose which dice to reroll, break if empty
            selected_dice = choose_dice_reroll(hand)
            if len(selected_dice) == 0:
                break

        selected_row = scoreboard.select_scoring(hand)
        scoreboard.assign_points(selected_row, hand)
        scoreboard.show_scoreboard_points()

        input("\nPress any key to continue")
        os.system('cls' if os.name == 'nt' else 'clear')

    print("\nCongratulations! You finished the game!\n")
    scoreboard.show_scoreboard_points()
    print("Total points: {}".format(sum(scoreboard.get_scoreboard_points())))


if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
