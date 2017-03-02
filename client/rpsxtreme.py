from random import randint
from time import sleep
from player import Player
from enums import Move, Outcome
from judge import Judge
from statistics import Statistics
from term_gfx import Graphics

debug = False

def show_moves(player):
    print("{}'s moves:\n1. Rocks: {}\n2. Paper: {}\n3. Scissors: {}\n".format(player.name,player.rocks,player.papers,player.scissors))
            
def get_player_choice(player):
    done = False
    choice = -1
    while not done:
        choice = input('What is your move?: ')
        if choice in ['q','quit','exit','fuck']:
            done = True
            choice = -1
        if choice in '123':
            choice = int(choice)
            choice -= 1 # minus one since choices do not begin with 0
            choice = choice % 3
            if player.can_choose_move(choice):
                done = True
    return choice

def get_random_from_list(l):
    return l[randint(0,len(l)-1)]

def get_players():
    player2 = Player(get_random_from_list(["Greger","Herman","Abraham", "Gunhilda", "Berit", "Handson"]))
    name = input("What is your name?: ")
    player1 = Player(name.capitalize() )
    return player1, player2

def get_opponent(retarded = False):
    return Player(get_random_from_list(["Greger","Herman","Abraham", "Gunhilda", "Berit", "Handson"]))

def match(p1,p2):
    judge = Judge()
    stats = Statistics(p1,p2)
    gfx = Graphics()

    gfx.battling_players(p1, p2)
    judge.on_start_of_match(p1, p2)
    for i in range(5):
        #judge.on_start_of_turn(p1,p2)
        
        # If a player has no more moves left match is over
        if not p1.has_moves_left() or not p2.has_moves_left():
            gfx.show_stats(stats)
            gfx.show_winner(stats)
            return

        # Begin turn and request choices
        
        gfx.show_stats(stats)
        gfx.show_moves(p1.get_moves())
        p1_choice = get_player_choice(p1)

        # if choice is -1, we wanted to exit.
        if p1_choice == -1:
            gfx.show_stats(stats)
            gfx.goodbye_screen()
            return
            
        
        p2_choice = judge.get_random_choice(p2)
        
        # Get outcome
        winner, loser, winner_move, loser_move = judge.determine_match_outcome(p1,
                                                                               p1_choice,
                                                                               p2,
                                                                               p2_choice)
        if (winner != None):
            judge.determine_match_fallout(winner, loser, winner_move, loser_move)
        else:
            judge.determine_draw_fallout(p1, p2, p1_choice, p2_choice)
    gfx.show_stats(stats)
    gfx.show_winner(stats)

if __name__ == '__main__':
    name = input("What is your name?: ")
    p1 = Player(name.capitalize())
    done = False
    gfx = Graphics()
    gfx.clear_screen()
    gfx.welcome_screen()
    while not done:
        p2 = get_opponent()
        match(p1,p2)
        answer = input('Are you done kicking ass? (y/n)')
        if answer in ['yes','yeah','yup','y']:
            done = True
