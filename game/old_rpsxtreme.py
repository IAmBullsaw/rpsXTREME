from random import randint
from time import sleep
from player import Player
from enums import Move, Outcome
from judge import Judge
from statistics import Statistics
from term_gfx import Graphics

debug = True

class RPSXGame:

    def __init__(self, p1, p2, judge):
        self.p1 = p1
        self.p2 = p2
        self.judge = judge
        self.stats = Statistics(p1, p2)
    
    def get_player_choice(self, player):
        done = False
        choice = -1
        while not done:
            choice = input('What is your move?: ')
            if choice in ['q','quit','exit']:
                done = True
                choice = -1
            if choice in '123':
                choice = int(choice)
                choice -= 1 # minus one since choices do not begin with 0
                choice = choice % 3
                if player.can_choose_move(choice):
                    done = True
        return choice

    def play(self):
        gfx = Graphics()

        gfx.battling_players(self.p1, self.p2)
        self.judge.on_start_of_match(self.p1, self.p2)
        for i in range(5):
            #judge.on_start_of_turn(p1,p2)
        
            # If a player has no more moves left match is over
            if not self.p1.has_moves_left() or not self.p2.has_moves_left():
                gfx.show_stats(self.stats)
                gfx.show_winner(self.stats)
                return

            # Begin turn and request choices
        
            gfx.show_stats(self.stats)
            gfx.show_moves(self.p1.get_moves())
            p1_choice = self.p1.get_chosen_move()#  get_player_choice(self.p1)

            # if choice is -1, we wanted to exit.
            if p1_choice == -1:
                gfx.show_stats(self.stats)
                gfx.goodbye_screen()
                return
        
        
            p2_choice = self.judge.get_random_choice(self.p2)
        
            # Get outcome
            winner, loser, winner_move, loser_move = self.judge.determine_match_outcome(self.p1,
                                                                                        p1_choice,
                                                                                        self.p2,
                                                                                        p2_choice)
            if (winner != None):
                self.stats.register_score(winner.get_name())
                self.judge.determine_match_fallout(winner, loser, winner_move, loser_move)
                gfx.show_player_won(winner)
            else:
                self.stats.register_score(None)
                self.judge.determine_draw_fallout(self.p1, self.p2, p1_choice, p2_choice)
                gfx.show_draw()
        gfx.show_stats(self.stats)
        gfx.show_winner(self.stats)


    def get_snapshot(self):
        return "{}".format(self.stats.pack_to_string())
    
