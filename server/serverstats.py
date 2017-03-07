import sys
import os
from timeit import default_timer as timer

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, '../game')

from enums import Move

class Serverstatistics:
    def __init__(self,timer_start):
        self.rocks = 0
        self.papers = 0
        self.scissors = 0
        self.tied_matches = 0
        self.matches = 0
        self.turns = 0
        self.tied_turns = 0
        self.timer_start = timer_start

    def new_match(self):
        self.matches += 1

    def move_played(self, move):
        if move == Move.ROCK:
            self.rocks += 1
        elif move == Move.PAPER:
            self.papers += 1
        elif move == Move.SCISSORS:
            self.scissors += 1
        else:
            pass

    def get_stats(self):
        return "{}|{}|{}|{}|{}".format(self.rocks,self.papers,self.scissors,self.ties,self.matches)

    def get_uptime(self):
        return timer() - self.timer_start

    def show_stats(self):
        print("\nStats:\tMoves played:")
        print("\tRocks: {}".format(self.rocks))
        print("\tPapers: {}".format(self.papers))
        print("\tScissors: {}".format(self.scissors))
        print("\tMatches:")
        print("\tTotal played: {}".format(self.matches))
        print("\tTied matches: {}".format(self.tied_matches))
        print("\tTotal turns: {}".format(self.turns))
        print("\tTotal tied turns: {}".format(self.tied_turns))
        print("\tServer uptime: {}".format(timer() - self.timer_start))
