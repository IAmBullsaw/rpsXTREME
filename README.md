# rpsXtreme

I had this Idea some time ago where one simple change of rules to Rock Paper Scissors would make a tournament possibly hilarious.

* The winner of a match gains the move his or her opponent lost with. The opponent loses this move as well.

So, for a tournament it is possible that the finale would end due to loss of possible moves.

In short I have here made a mock up in python 3 of the game, a client and server for a network based tournament.

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

The main idea is that the server is responsible for matching 2 users, using the client,  and let them play one match. Matches are run on the server, not with the client. When a match is over, the users can request to play one more with another random user.

Both client and server make use of python's socket module.

## Client

I have been thinking of implementing a graphical user interface to be used instead of a terminal. But right now, I focus on a client for use in a terminal. First things first, you know?

Where it's at now:

* Client connects to server.
* Client requests a match.
* Client receives snapshots of the match.
* Client answers to Move requests from server.

No user input is handled yet. However the client has a rock solid plan: Only play rock...

## Server

Where it's at now:

* Server opens socket for everyone. Everyone.
* Server connects with client.
* Server responds to match request and starts a new bot match.
* Server sends snapshots of the match to correct client.
* Server can send snapshots of up to 9 turns before client crashes and that crash crashes the server. But it's OK, we don't need more than 5 turns :D (Crash occurs sincesend-limit is exceeded)

# Known bugs

* It's literally unplayable.
