#!/usr/bin/env python

"""Yahtzee, the board game!

This python program will simulate a game of Yahtzee
"""

import sys
import os
import random
import re
from hand import Die, Hand
from rules import Rules

class ScoreBoard(object):

    # TODO: Everything
    def __init__(self):
        self.scoreboard_rows = {
            1: "Aces",
            2: "Twos",
            3: "Threes",
            4: "Fours",
            5: "Fives",
            6: "Sixes",
            7: "Three of a Kind",
            8: "Four of a Kind",
            9: "Full House",
            10: "Small Straight",
            11: "Large Straight",
            12: "Yahtzee",
            13: "Chance",
        }
        # Once again, prevent cheating with private variables
        self.__scoreboard_points = {}

    def set_scoreboard_row_value(self, row, value):
        if row not in self.scoreboard_rows.keys():
            print("Bad row index")
            return False
        else:
            if row in self.__scoreboard_points.keys():
                print("ScoreBoard already saved!")
                return False
            else:
                print("Adding {} points to {}".format(
                    value,
                    self.scoreboard_rows[int(row)])
                )
                self.__scoreboard_points[row] = value
                return True

    def get_scoreboard_points(self):
        return self.__scoreboard_points

    def show_scoreboard_rows(self):
        for key, val in self.scoreboard_rows.items():
            print("{}. {}".format(key, val))

    def show_scoreboard_points(self):
        print("\nSCOREBOARD")
        print("===================================")
        for idx, row in self.scoreboard_rows.items():
            try:
                print("{:<2} {:<21}| {:2} points".format(idx+1,
                      row,
                      self.__scoreboard_points[idx]))
            except KeyError:
                print("{:<2} {:<21}|".format(idx+1, row))
        print("===================================")

    def select_scoring(self, hand):
        msg = "Choose which scoring to use "\
               "(leave empty to show available rows): "
        scoreboard_row = False
        score_saved = False
        while not scoreboard_row and not score_saved:
            scoreboard_row = input(msg)
            if scoreboard_row.strip() == "":
                self.show_scoreboard_points()
                scoreboard_row = False
                continue
            try:
                scoreboard_row = int(re.sub('[^0-9,]', '', scoreboard_row))
            except ValueError:
                print("You entered something other than a number.")
                print("Please try again")
                scoreboard_row = False
                continue
            if scoreboard_row > len(self.scoreboard_rows):
                print("Please select an existing scoring rule.")
                scoreboard_row = False
                continue
            else:
                score_saved = self.set_scoreboard_row_value(
                    int(scoreboard_row),
                    Rules().rules_map[int(scoreboard_row)](hand)
                )

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
                return list(map(int, reroll))  # Turn strings in list to int
            
            if not reroll or 0 in reroll:
                return []

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
    while len(scoreboard.get_scoreboard_points()) < len(scoreboard.scoreboard_rows):
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
                print("Braking out because len == 0")
                break

        scoreboard.select_scoring(hand)
        scoreboard.show_scoreboard_points()

        input("\nPress any key to continue")
        os.system('cls' if os.name == 'nt' else 'clear')

    print("\nCongratulations! You finished the game!\n")
    scoreboard.show_scoreboard_points()
    print("Total points: {}".format(sum(scoreboard.get_scoreboard_points().values())))


if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        print("\nExiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
