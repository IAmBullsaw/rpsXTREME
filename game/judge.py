from random import randint
from enums import Move

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
            return None, None, None, None
        
        if (p1move == Move.ROCK and p2move == Move.SCISSORS):
            return p1, p2, p1move, p2move
        elif (p1move == Move.PAPER and p2move == Move.ROCK ):
            return p1, p2, p1move, p2move
        elif (p1move == Move.SCISSORS and p2move == Move.PAPER):
            return p1, p2, p1move, p2move
        else:
            return p2, p1, p2move, p1move
        
    def on_start_of_turn(self,p1,p2):
        p1.gain_move([Move.PAPER,Move.ROCK,Move.SCISSORS][randint(0,2)])
        p2.gain_move([Move.PAPER,Move.ROCK,Move.SCISSORS][randint(0,2)])

    def on_start_of_match(self,p1,p2):
        pass
        
    def determine_match_fallout(self,winner,loser,winner_move,loser_move):
        winner.gain_move(loser_move)
        loser.lose_move(loser_move)
        
        winner.gain_points(2)

    def determine_draw_fallout(self,player1,player2,p1move,p2move):
        player1.gain_points(1)
        player2.gain_points(1)
        pass
        
    def determine_loss_fallout(self,winner,loser,p1move,p2move):
        loser.lose_move(p1move)

    def bribe(self,who):
        self.bribed = (True, who)

    def get_random_choice(self,player):
        done = False
        
        choice = -1
        if not player.has_moves_left():
            return choice

        while not done:
            choice = randint(0,2)
            if player.can_choose_move(choice):
                done = True
        
        return choice
