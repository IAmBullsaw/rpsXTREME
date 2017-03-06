from enum import Enum
class Move(Enum):
    ROCK = 10
    PAPER = 20
    SCISSORS = 30

    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ == int:
            return self.value == other
        else:
            return NotImplemented

    def encode(self, encoding = 'ascii'):
        return str(self.value).encode(encoding)

    def decode(encoded, encoding = 'ascii'):
        if encoded == (Move.ROCK).encode(encoding):
            return Move.ROCK
        elif encoded == (Move.PAPER).encode(encoding):
            return Move.PAPER
        elif encoded == (Move.SCISSORS).encode(encoding):
            return Move.SCISSORS
        else:
            print(encoded)
            NotImplemented

    def to_enum(number):
        if number == 10:
            return Move.ROCK
        elif number == 20:
            return Move.PAPER
        elif number == 30:
            return Move.SCISSORS
        else:
            return None
            
    
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
    REQUEST_SNAPSHOT = 60
    MATCH_OVER = 70
    
    def __eq__(self,other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ == int:
            return self.value == other
        else:
            return NotImplemented
        
    def encode(self,encoding = 'ascii'):
        return str(self.value).encode(encoding)

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
        elif encoded == (Command.REQUEST_SNAPSHOT).encode(encoding):
            return Command.REQUEST_SNAPSHOT
        elif encoded == (Command.MATCH_OVER).encode(encoding):
            return Command.MATCH_OVER
        else:
            NotImplemented
            
