# rpsXtreme

I had this Idea some time ago where one simple change of rules to Rock Paper Scissors would make a tournament possibly hilarious.

* The winner of a match gains the move his or her opponent lost with. The opponent loses this move as well.

So, for a tournament it is possible that the finale would end due to loss of possible moves.

## Rules and definitions

* A turn is one standard game of rock paper scissors.
* A match is set of 5 turns.
* A player starts with 1 rock, 1 paper, 1 scissors.
* A player is not allowed to use a move if he or she has zero or less moves of this kind left.
* A player loses if the player has no moves left.

Points

* A player gains 10 points for a won match.
* A player gains 2 points for a tied match.
* A player gains 2 points for a won turn.
* A player gains 1 point for a tied turn.
* A player never loses points.

## Additional rules

Alternative rules has been discussed en masse, some of them reaches this list
* Giving a player a random move at the beginning of each match (or turn).
* There should be a, usable only once, "nuke move" for each player to overrule original match outcome and make sure you win that turn.

# Server and client

What first seemed to be a stupid idea evolved even further.
I have a raspberry pi and figured I should make this game into some online rpsxtreme game, because rpsXtreme is super fun.

Idea: The server is responsible for matching 2 users and let them play a match. then they can request to play one more with another random user.

connection protocol:
client:
´´´
connect
send player data
recv match connected and who to battle
match_continues = True
while match_continues:
    send turn move
    recv turn outcome and stats and recvd_match_continues
    match_continues = recvd_match_continues
´´´