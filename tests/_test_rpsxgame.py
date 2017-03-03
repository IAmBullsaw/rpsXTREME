import sys
sys.path.insert(0,'../game')
sys.path.insert(0,'../server')
sys.path.insert(0,'../client')

from rpsxtreme import RPSXGame
from player import Player
from judge import Judge
from rpsxserver import RPSXServer

def plp(test):
    print('\t',test,'\tPassed')

def test_RPSXGame():
    p1 = Player('p1',bot=True)
    bot = Player('p2',bot=True)
    game = RPSXGame(p1,bot,Judge())
    for i in range(10):
        game.play()
    plp('test_RPSXGame()')

def test_RPSXServer():
    plp('test_RPSXServer()')
    server = RPSXServer('',port = 5000)
    server.run()
    pass
    
if __name__ == '__main__':
    test_RPSXGame()
    test_RPSXServer()
