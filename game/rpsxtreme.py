from enums import Move
from judge import Judge
from player import Player
from statistics import Statistics

debug = True

def pl(message,t=True):
    if debug:
        if t:
            print("\t" + str(message))
        else:
            print(str(message))

class RPSXGame:

    def __init__(self,p1,p2,judge,bot=False):
        self.p1 = p1
        self.p2 = p2
        self.p1_move = None
        self.p2_move = None
        self.judge = judge
        self.stats = Statistics(p1,p2)
        self.winner = None
        self.bot_match = bot
        
    def set_p1_move(self,move):
        self.p1_move = move

    def set_p2_move(self,move):
        self.p2_move = move

    def reset_moves(self):
        self.p1_move = None
        self.p2_move = None
            
    def get_snapshot(self):
        return "{}:{}:{}".format(self.p1.pack_to_string(),
                                 self.p2.pack_to_string(),
                                 self.stats.pack_to_string())
    def play(self):
        pl("Playing {} against {}".format(self.p1_move,self.p2_move))

        if self.bot_match:
            self.p2_move = self.p2.get_chosen_move()
        
        if not self.p1_move or not self.p2_move:
            raise Exception("All moves arent set")

        self.judge.on_start_of_match(self.p1, self.p2)
        winner, loser, winner_move, loser_move = self.judge.determine_match_outcome(self.p1,
                                                                                    self.p1_move,
                                                                                    self.p2,
                                                                                    self.p2_move)
        if (winner != None):
            self.stats.register_score(winner.get_name())
            self.judge.determine_match_fallout(winner, loser, winner_move, loser_move)
        else:
            self.stats.register_score(None)
            self.judge.determine_draw_fallout(self.p1,
                                              self.p2,
                                              self.p1_move,
                                              self.p2_move)
        self.reset_moves()

    def finish(self):
        self.winner = self.stats.get_match_winner()

    def get_winner(self):
        return self.winner
        
if __name__ == '__main__':
    print("Testing game")
    p1 = Player('p1')
    p2 = Player('p2')
    match = RPSXGame(p1,p2,Judge())
    match.set_p1_move(Move.ROCK)
    match.set_p2_move(Move.PAPER)
    match.play() # P2 should win
    score = match.get_snapshot().split('\\')[2]
    pl("p2 wins: " + score[1] == '1')
    match.set_p1_move(Move.ROCK)
    match.set_p2_move(Move.ROCK)
    match.play() # Should be a tie
    score = match.get_snapshot().split('\\')[2]
    pl("'twas a tie: " + score[4] == '0')
    match.finish()
    winner = match.get_winner()
    pl("Winner is: {}".format(winner))
