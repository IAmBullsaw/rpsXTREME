from random import randint
from enums import Move

class Player:
    def __init__(self, name, retarded = False):
        self.name = name + self.get_power_name()
        self.rocks = 1 if not retarded else 0
        self.papers = 1 if not retarded else 0
        self.scissors = 1
        self.points = 0
        self.wins = 0

    def get_power_name(self):
        l = ["the Defiler","the Crusher of Hands","of Doom","the Hand Magician"]
        return " " + l[randint(0, len(l)-1)]
        
    def lose_move(self, move):
        if (move == Move.ROCK):
            self.rocks -= 1
        elif (move == Move.PAPER):
            self.papers -= 1
        elif (move == Move.SCISSORS):
            self.scissors -= 1

    def gain_move(self,move):
        if (move == Move.ROCK):
            self.rocks += 1
        elif (move == Move.PAPER):
            self.papers += 1
        elif (move == Move.SCISSORS):
            self.scissors += 1
        else:
            NotImplemented
            
    def won_match(self):
        self.wins += 1

    def gain_points(self, points):
        self.points += points

    def get_moves(self):
        return [self.rocks,self.papers, self.scissors]

    def get_points(self):
        return self.points

    def get_wins(self):
        return self.wins
        
    def get_name(self):
        return self.name

    def is_retarded(self):
        return self.retarded

    def has_moves_left(self):
        return (self.rocks > 0 or self.papers > 0 or self.scissors > 0)
        
    def can_choose_move(self, move):
        if move == Move.ROCK:
            return self.rocks > 0
        elif move == Move.PAPER:
            return self.papers > 0
        else:
            return self.scissors > 0
