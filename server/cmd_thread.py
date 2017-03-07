import threading

class Cmdthread(threading.Thread):
    def __init__(self, threadID, name, stats):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.stats = stats
      self.daemon = True
      
    def run(self):
        done = False
        while not done:
            cmd = input("enter 'ss' for stats:\t")
            if cmd == 'ss':
                self.stats.show_stats()
                
    
