from enum import Enum
class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ == int:
            return self.value == other
        else:
            return NotImplemented   
    
class Outcome(Enum):
    WON = 0
    DRAW = 1
    LOST = 2

    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ == int:
            return self.value == other
        else:
            return NotImplemented
