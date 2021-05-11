import random


class Die:

    def __init__(self, face: int = None, sides: int = 6):
        self.sides = sides
        if face is not None:
            self.__face = face
        else:
            self.roll() # Arjan: call roll immediately (die always has a face up)

    def roll(self):
        # ARJAN: Random now uses the number of sides and returns the face
        self.__face = random.randint(1, self.sides)
        return self.__face

    def set_face(self, value):
        self.__face = value

    def get_face(self):
        return self.__face

    def __str__(self):
        return str(self.__face)

class Hand:

    def __init__(self, dice=5, sides=6):
        self.dice = dice
        self.hand = []
        for _ in range(dice):
            self.hand.append(Die(None, sides))

    def all_dice(self):
        return range(1, self.dice + 1)

    def roll(self, dice):
        if [x for x in dice if x > self.dice]:
            raise IndexError(f"You only have {self.dice} dice!")
        for i in dice:
            self.hand[i-1].roll()

    def get_hand(self):
        return [die.get_face() for die in self.hand]

    def set_faces(self, values):
        for idx, val in enumerate(values):
            self.hand[idx].set_face(val)
    
    def count(self, i):
        return self.get_hand().count(i)

    def sum(self):
        return sum(self.get_hand())

    def __str__(self):
        return '\n'.join([f"die {idx + 1} has value {die}" for idx, die in enumerate(self.hand)])
