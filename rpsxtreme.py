
from random import randint
from time import sleep
from player import Player
from enums import Move, Outcome
from judge import Judge
from statistics import Statistics

debug = False

def show_moves(player):
        print("{}'s moves:\n1. Rocks: {}\n2. Paper: {}\n3. Scissors: {}\n".format(player.name,player.rocks,player.papers,player.scissors))
            
def get_player_choice(player):
        done = False
        if not player.has_moves_left():
            return -1

        choice = -1
        while not done:
            choice = int(input('What is your move?: ')) - 1 # minus one since choices do not begin with 0
            choice = choice % 3
            if player.can_choose_move(choice):
                done = True
                
        return choice

def clear_screen():
    print("\n" * 100)

def get_random_from_list(l):
    return l[randint(0,len(l)-1)]
        
def main(debug = False):
    clear_screen()
    
    judge = Judge()
    player2 = Player(get_random_from_list(["Greger","Herman","Abraham", "Gunhilda", "Berit", "Handson"]))
    done = False

    print("Welcome to rpsEXTREME")
    name = input("What is your name?: ")
    player1 = Player(name)

    stats = Statistics(player1, player2)
    while not done:
        print("You are battling {}".format(player2.get_name()))
        show_moves(player1)
        p1_choice = get_player_choice(player1)
        p2_choice = judge.get_random_choice(player2)

        if p1_choice < 0 or p2_choice < 0:
            done = True
        else:
            outcome, winner, loser, winner_move, loser_move = judge.determine_match_outcome(player1, p1_choice, player2, p2_choice)
            
            if (outcome != Outcome.DRAW):
                print("The winner is: {}".format(winner.get_name()))
                judge.determine_match_fallout(winner,loser, winner_move, loser_move)
            else:
                print("IT WAS A DRAW!")
            stats.show()
            if not debug:
                sleep(1.5)
                clear_screen()
    stats.show()
    stats.show_winner()

def pseudo():
    judge = Judge()
    p1, p2 = get_players()

    judge.on_start_of_match(p1,p2)
    for i in range(5):
        judge.on_start_of_turn(p1,p2)

        # Begin turn and request choices
        p1_choice = get_player_choice(p1)
        p2_choice = judge.get_random_choice(p2)

        # 
    
if __name__ == '__main__':
    main(debug = False)
