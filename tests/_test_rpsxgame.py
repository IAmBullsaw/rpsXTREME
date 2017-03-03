import sys
sys.path.insert(0,'../game')
from rpsxtreme import RPSXGame
from player import Player
from judge import Judge

def test():
    p1 = Player('p1')
    bot = Player('p2',bot=True)
    game = RPSXGame(p1,bot,Judge())
    game.play()
    
if __name__ == '__main__':
    test()
