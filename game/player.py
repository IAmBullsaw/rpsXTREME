from random import randint
from enums import Move

class Player:
    def __init__(self, name = None, bot = False):
        self.name = name.capitalize() + self.get_power_name()
        self.rocks = 1
        self.papers = 1 
        self.scissors = 1
        self.points = 0
        self.wins = 0
        self.bot = bot

    def get_power_name(self):
        l = ["the Defiler","the Crusher of Hands","of Doom","the Hand Magician", "the Rock", "the Paperbag King", "Scissorhands"]
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

    def has_moves_left(self):
        return (self.rocks > 0 or self.papers > 0 or self.scissors > 0)
        
    def can_choose_move(self, move):
        if move == Move.ROCK:
            return self.rocks > 0
        elif move == Move.PAPER:
            return self.papers > 0
        else:
            return self.scissors > 0

    def get_chosen_move(self):
        choice = None

        if not self.has_moves_left():
            return choice
        
        done = False
        if not self.bot:
            self.print_moves()
            while not done:
                choice = input('\tWhat is your move?: ')
                if not choice or choice == '':
                    pass
                elif choice in ['q','quit','exit']:
                    done = True
                    choice = None
                elif choice in '123':
                    choice = int(choice)
                    choice -= 1 # minus one since choices do not begin with 0
                    choice = choice % 3
                    choice = Move.to_enum(choice)
                    if self.can_choose_move(choice):
                        done = True
        else:
            while not done:
                choice = randint(0,2)
                choice = Move.to_enum(choice)
                print("chose: {}".format(choice))
                if self.can_choose_move(choice):
                    done = True
        return choice
        
    def pack_to_string(self):
        return "{}|{}|{}|{}|{}|{}".format(self.name,
                                          self.rocks,
                                          self.papers,
                                          self.scissors,
                                          self.points,
                                          self.wins)

    def unpack_from_string(self,string):
        self.name,self.rocks,self.papers,self.scissors,self.points,self.wins = string.split('|')
        self.rocks = int(self.rocks)
        self.papers = int(self.papers)
        self.scissors = int(self.scissors)
        self.points = int(self.points)
        self.wins = int(self.wins)

    def print_moves(self):
        print("\n\tMake a choice!\n\t1. Rocks left: {}\n\t2. Papers left: {}\n\t3. Scissors left: {}".format(self.rocks,self.papers,self.scissors))

    def __repr__(self):
        return "<player " + self.pack_to_string() +'>'

    def reset_moves(self):
        self.rocks = 1
        self.scissors = 1
        self.papers = 1

#######
# Tests
def test():
    p = Player('p')
    s = p.pack_to_string()
    p2 = Player('p2')
    p2.unpack_from_string(s)
    print('Names are equal after unpack: ',p.get_name() == p2.get_name())
    
if __name__ == '__main__':
    test()
