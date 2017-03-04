
class Graphics:

    def __init__(self):
        self.divider = "*" * 50
    
    def clear_screen(self):
        print("\n" * 100)
        
    def welcome_screen(self):
        print(self.divider)
        print(" "*12,"Welcome to rpsXtreme!")
        print(self.divider)

    def goodbye_screen(self):
        print(self.divider)
        print(" "*12,"Too Xtreme for you?")
        print(" "*12,"See you next time!")
        print(self.divider)
        

    def battling_players(self,p1,p2):
        print(self.divider)
        print("Welcome to this match of rpsXtreme!")
        print("This match is between")
        print("\n\t{} VS. {}\n".format((p1.get_name()).capitalize(), p2.get_name()) )
        print("FIGHT!")
        print(self.divider)

    def show_moves(self,moves):
        print("Current moves:\n1. Rocks: {}\n2. Papers: {}\n3. Scissors {}".format(moves[0],
                                                                                   moves[1],
                                                                                   moves[2]))
    def show_player_won(self,player):
        print(self.divider)
        print("The winner of the turn is: {}".format(player.get_name()))
        print(self.divider)

    def show_draw(self):
        print(self.divider)
        print("IT WAS A DRAW!")
        print(self.divider)
        
    def show_stats(self, stats):
        stats.show()
        
    def show_winner(self, stats):
        stats.show_winner()

    def show_snapshot(self,snapshot):
        print("\n\tSnapshot:")
        p1, p2, match = snapshot.split('|')
        print("\tp1 vs p2")
        print('\t'+match+'\n')
