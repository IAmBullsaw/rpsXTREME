class Statistics:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        
    def show(self):
        if (self.p1).get_points() > (self.p2).get_points():
            print("Current stats:\n{}: {}\n{}: {}".format((self.p1).get_name(),
                                                          (self.p1).get_points(),
                                                          (self.p2).get_name(),
                                                          (self.p2).get_points()) )
        else:
            print("Current stats:\n{}: {}\n{}: {}".format((self.p2).get_name(),
                                                          (self.p2).get_points(),
                                                          (self.p1).get_name(),
                                                          (self.p1).get_points()) )
    def show_winner(self):
        if (self.p1).get_points() > (self.p2).get_points():
            print("Winner of this round: {} with {} points!".format((self.p1).get_name(),
                                                                    (self.p1).get_points() ))
        else:
            print("Winner of this round: {} with {} points!".format((self.p2).get_name(),
                                                                    (self.p2).get_points() ))
