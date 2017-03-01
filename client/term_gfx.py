
class Graphics:

    def __init__(self):
        self.divider = "*" * 50
    
    def clear_screen(self):
        print("\n" * 100)
        
    def welcome_screen(self):
        print(self.divider)
        print(" "*12,"Welcome to rpsEXTREME")
        print(self.divider)

    def goodbye_screen(self):
        print(self.divider)
        print(" "*12,"Too Xtreme for you?")
        print(" "*12,"See you next time!")
        print(self.divider)
        

    def battling_players(self,p1,p2):
        print("Right now, this match is between")
        print("\n{} vs {}\n".format((p1.get_name()).capitalize(), p2.get_name()) )

    def show_moves(self,moves):
        print("Current moves:\n1. Rocks: {}\n2. Papers: {}\n3. Scissors {}".format(moves[0],
                                                                                   moves[1],
                                                                                   moves[2]))
    def show_winner(self,player):
        print("The winner of the turn is: {}".format(player.get_name()))

    def show_draw(self):
        print(self.divider)
        print("IT WAS A DRAW!")
        print(self.divider)
        
    def show_stats(self, stats):
        stats.show()
        
    def show_winner(self, stats):
        stats.show_winner()
