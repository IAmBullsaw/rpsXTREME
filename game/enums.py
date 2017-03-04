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

class Command(Enum):
    CLOSE = 10
    OK = 20
    REQUEST_GAME = 30
    REQUEST_MOVE = 40
    REQUEST_PLAYER = 50
    
    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ == int:
            return self.value == other
        else:
            return NotImplemented
        
    def __str__(self):
        return str(self.value)

    def encode(self,encoding = 'ascii'):
        return str(self).encode(encoding)

    # Decodes an encoded enum. This feels horrible.
    def decode(encoded, encoding = 'ascii'):
        if encoded == (Command.CLOSE).encode(encoding):
            return Command.CLOSE
        elif encoded == (Command.OK).encode(encoding):
            return Command.OK
        elif encoded == (Command.REQUEST_GAME).encode(encoding):
            return Command.REQUEST_GAME
        elif encoded == (Command.REQUEST_MOVE).encode(encoding):
            return Command.REQUEST_MOVE
        elif encoded == (Command.REQUEST_PLAYER).encode(encoding):
            return Command.REQUEST_PLAYER
        else:
            NotImplemented
            
