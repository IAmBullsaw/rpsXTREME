class Statistics:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.score = [] # 0 = draw, -1 = p1 won, +1 = p2 won

    def register_score(self,winner):
        if not winner:
            self.score.append(0)
        elif self.p1.get_name() == winner:
            self.score.append(-1)
        else:
            self.score.append(1)

    def get_score(self):
        return self.score

    def get_match_winner(self):
        matches = len(self.score)
        total = sum(self.score)
        if total < 0:
            return self.p1
        elif total > 0:
            return self.p2
        else:
            return None
            
    def show(self):
        if (self.p1 and self.p2) and (self.p1).get_points() > (self.p2).get_points():
            print("\tCurrent stats:\n\t{}: {}\n\t{}: {}".format((self.p1).get_name(),
                                                          (self.p1).get_points(),
                                                          (self.p2).get_name(),
                                                          (self.p2).get_points()) )
        else:
            print("\tCurrent stats:\n\t{}: {}\n\t{}: {}".format((self.p2).get_name(),
                                                          (self.p2).get_points(),
                                                          (self.p1).get_name(),
                                                          (self.p1).get_points()) )
    def show_winner(self):
        if (self.p1).get_points() > (self.p2).get_points():
            print("Winner of this match: {} with {} points!".format((self.p1).get_name(),
                                                                    (self.p1).get_points() ))
        else:
            print("Winner of this match: {} with {} points!".format((self.p2).get_name(),
                                                                    (self.p2).get_points() ))

    def pack_to_string(self):
        msg = [str(p)+'2' for p in self.score]
        return "{}".format(msg[0:-1])

    def load_from_string(self,string):
        l = string.split('2')

        self.score = []
        if not l == '[]':
            for e in l:
                if not e in '[]':
                    self.score.append(int(e))
                

    def show_last_turn_winner(self):
        last = self.get_last_score()
        padding = '\t'
        if last:
            if last == 0:
                print(padding + "It was a tie.")
            elif last > 0:
                print(padding + "{} won this turn.".format(self.p2.get_name()))
            else:
                print(padding + "{} won this turn.".format(self.p1.get_name()))

    def get_last_score(self):
        last = None
        if len(self.score) > 0:
            last = self.score[-1]
        return last
