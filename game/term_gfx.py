from player import Player
from statistics import Statistics
def pl(msg):
    print('\t'+msg)

class Graphics:

    def __init__(self):
        self.divider = "*" * 50
        
    def clear_screen(self):
        print("\n" * 100)
        
    def welcome_screen(self):
        pl(self.divider)
        pl(" "*12,"Welcome to rpsXtreme!")
        pl(self.divider)

    def goodbye_screen(self):
        pl(self.divider)
        pl(" "*12,"Too Xtreme for you?")
        pl(" "*12,"See you next time!")
        pl(self.divider)
        

    def battling_players(self,p1,p2):
        pl(self.divider)
        pl("Welcome to this match of rpsXtreme!")
        pl("This match is between")
        pl("\n\t{} VS. {}\n".format((p1.get_name()).capitalize(), p2.get_name()) )
        pl("FIGHT!")
        pl(self.divider)

    def show_moves(self,moves):
        pl("Current moves:\n1. Rocks: {}\n2. Papers: {}\n3. Scissors {}".format(moves[0],
                                                                                   moves[1],
                                                                                   moves[2]))
    def show_player_won(self,player):
        pl(self.divider)
        pl("The winner of the turn is: {}".format(player.get_name()))
        pl(self.divider)

    def show_draw(self):
        pl(self.divider)
        pl("IT WAS A DRAW!")
        pl(self.divider)
        
    def show_stats(self, stats):
        stats.show()
        
    def show_winner(self, stats):
        stats.show_winner()

    def show_snapshot(self,snapshot):
        pl('')
        p1, p2, stats = snapshot.split(':')

        # Todo:
        # Fix this horrible thing
        # it should only exist for a short period of time
        # come on....
        # do it.
        
        pl1 = Player('')
        pl2 = Player('')
        pl1.unpack_from_string(p1)
        pl2.unpack_from_string(p2)
        pl("{} VS {}".format(pl1.get_name(),pl2.get_name()))
        s = Statistics(pl1,pl2)
        s.load_from_string(stats)
        s.show()
        s.show_last_turn_winner()
