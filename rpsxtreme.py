from enum import Enum
from random import randint

class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ == int:
            return self.value == other
        else:
            return NotImplemented   
    
class Outcome(Enum):
    WON = 0
    DRAW = 1
    LOST = 2

    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ == int:
            return self.value == other
        else:
            return NotImplemented

class Player:
    def __init__(self,name):
        self.name = name
        self.rocks = 1
        self.papers = 1
        self.scissors = 1
        self.points = 0

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
            print("What the fuck is: " + str(move))

    def gain_points(self, points):
        self.points += points
            
    def show_moves(self):
        print("{}'s moves:\n1. Rocks: {}\n2. Paper: {}\n3. Scissors: {}\n".format(self.name,self.rocks,self.papers,self.scissors))

    def get_points(self):
        return self.points
        
    def get_name(self):
        return self.name;

    def has_moves_left(self):
        return (self.rocks > 0 or self.papers > 0 or self.scissors > 0)
        
    def can_choose_move(self, move):
        if move == Move.ROCK:
            return self.rocks > 0
        elif move == Move.PAPER:
            return self.papers > 0
        else:
            return self.scissors > 0
            
class Judge:
    def __init__(self):
        self.bribed = (False,None)
        
    def allowed_move(self,player,move):
        if (move == Move.ROCK and player.rocks > 0):
            return True
        elif (move == Move.PAPER and player.papers > 0):
            return True
        elif (move == Move.SCISSORS and player.scissors > 0):
            return True
        else:
            return False
    
    def determine_match_outcome(self,p1,p1move,p2,p2move):
        if (p1move == p2move):
            return Outcome.DRAW, None, None
        
        if (p1move == Move.ROCK and p2move == Move.SCISSORS):
            return Outcome.WON, p1, p2
        elif (p1move == Move.PAPER and p2move == Move.ROCK ):
            return Outcome.WON, p1, p2    
        elif (p1move == Move.SCISSORS and p2move == Move.PAPER):
            return Outcome.WON, p1, p2
        else:
            return Outcome.WON, p2, p1

    def determine_win_fallout(self,player,p1move,p2move):
        player.gain_move(p2move)
        player.gain_points(1)

    def determine_loss_fallout(self,player,p1move,p2move):
        player.lose_move(p1move)

    def bribe(self,who):
        self.bribed = (True, who)

    def get_random_choice(self):
        return randint(0,2)

    def get_player_choice(self,player):
        done = False
        if not player.has_moves_left():
            return -1

        choice = -1
        while not done:
            choice = int(input('What is your move?: ')) - 1 # minus one since choices do not begin with 0
            if player.can_choose_move(choice):
                done = True
                
        return choice
            
def main(debug = False):

    judge = Judge()
    player2 = Player("Greger of Doom")
    done = False

    print("Welcome to rpsEXTREME")
    name = input("What is your name?: ")
    player1 = Player(name) 
    while not done:
        print("You are battling {}".format(player2.get_name()))
        print("Current stats:\n{}: {}\n{}: {}".format(player1.get_name(),player1.get_points(),player2.get_name(),player2.get_points()) )
        player1.show_moves()
        p1_choice = judge.get_player_choice(player1)
        p2_choice = judge.get_random_choice()

        if p1_choice < 0:
            done = True
        else:
            outcome, winner, loser = judge.determine_match_outcome(player1, p1_choice, player2, p2_choice)
            
            if debug:
                print("\n*********DEBUG**********")
                if outcome != Outcome.DRAW:
                    print('Outcome:',outcome,'\nwinner:',winner.get_name(),'\nloser:',loser.get_name(),'\np1_choice:', p1_choice,'\np2_choice:', p2_choice)
                else:
                    print('Outcome:',outcome,'\nwinner:',winner,'\nloser:',loser,'\np1_choice:', p1_choice,'\np2_choice:', p2_choice)
                    print("*********DEBUG**********\n")
                
            if (outcome != Outcome.DRAW):
                print("The winner is: {}".format(winner.get_name()))
                judge.determine_win_fallout(winner,p1_choice,p2_choice)
                judge.determine_loss_fallout(loser,p1_choice,p2_choice)
            else:
                print("IT WAS A DRAW!")


    print("Final stats:\n{}: {}\n{}: {}".format(player1.get_name(),player1.get_points(),player2.get_name(),player2.get_points()) )

if __name__ == '__main__':
    main(debug = True)
