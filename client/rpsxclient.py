import sys
import os
from time import sleep

# When running as a script cwd is not script dir.
# Change cwd to dir where this file is...
os.chdir(os.path.dirname(__file__))

sys.path.insert(0, '../game')

import socket
from term_gfx import Graphics
from player import Player
from enums import Command, Move
debug = True

def pl(msg):
    if debug:
        print("\t" + msg)

class RPSXClient:
    def __init__(self, player, host='155.4.151.254', port = 4711):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.player = player
        self.gfx = Graphics()

    def connect(self):
        pl("connecting to {}:{}".format(self.host,self.port))
        try:
            self.sock.connect((self.host,self.port))
        except:
            pl("Couldn't establish connection")
            raise Exception("Couldn't establish connection")
        pl("connected")
        self.welcome()

    def close(self):
        pl("Closing connection to {}:{}".format(self.host,self.port))
        self.sock.close()

    def save_state(self):
        pass

    def welcome(self):
        message = "Welcome to rpsXtreme!"
        l = len(message)+22
        pl("*"*l)
        pl("*"+" "*10+message+" "*10+"*")
        pl("*"*l)
    
    def goodbye(self):
        message = "Goodbye for now..."
        l = len(message)+22
        pl("*"*l)
        pl("*"+" "*10+message+" "*10+"*")
        pl("*"*l)
        
    def tear_down(self):
        self.close()
        self.save_state()
        self.goodbye()

    def connection_lost(self):
        pass
        
    def send_player(self,player):
        msg = player.pack_to_string()
        pl("Send: {}...".format(msg))
        self.sock.send(msg.encode('ascii'))

    def recv_start_match_data(self):
        pl("recv_start_match_data")
        msg = self.sock.recv(1024)
        pl(msg.decode('ascii'))

    def send_cmd(self,cmd):
        pl("Send: {}".format(cmd))
        self.sock.send(cmd.encode('ascii'))

    def send_mov(self,mov):
        self.send_cmd(mov)
        
    def recv_cmd(self):
        pl("waiting for command...")
        cmd = self.sock.recv(10)
        cmd = Command.decode(cmd)
        pl("recv: {}".format(cmd))
        return cmd

    def recv_snapshot(self):
        pl("recv: snapshot")
        ans = self.sock.recv(100)
        return ans.decode('ascii')

    def snapshot_transaction(self,ans_cmd = Command.OK):
        snapshot = self.recv_snapshot()
        self.send_cmd(ans_cmd)
        return snapshot
    

    def cmd_transaction(self,send_cmd,ans_cmd = Command.OK):
        pl("Transaction: send {} recv{}".format(send_cmd,ans_cmd))
        self.send_cmd(send_cmd)
        cmd = self.recv_cmd()
        if not cmd or cmd == '':
            pl("Transaction failed. Connection closed unexpectedly")
        if not cmd == ans_cmd:
            raise Exception("Transaction failed. Expected {} received {}".format(send_cmd,ans_cmd))
        
    def mov_transaction(self,send_mov, ans_cmd = Command.OK):
        pl("Transaction: send {} recv{}".format(send_mov,ans_cmd))
        self.send_mov(send_mov)
        cmd = self.recv_cmd()
        if not cmd or cmd == '':
            pl("Transaction failed. Connection closed unexpectedly")
        if not cmd == ans_cmd:
            raise Exception("Transaction failed. Expected {} received {}".format(send_cmd,ans_cmd))

    def play(self):
        """
        1. send: request game
        2. recv: OK
        3. send: request snapshot
        3. recv: get snapshot
        4. send: OK
        
        while not done
        4. recv: get request for move
        5. send: move
        6. recv: ok
        7. recv: turn outcome / match outcome
        
        """
        pl("requesting game...")

        self.cmd_transaction(Command.REQUEST_GAME)
        # Main game loop
        self.main_game_loop()
        # Loop done, match over.
        self.tear_down()


    def play_turn(self):
        """
         Request snapshot
         Receive OK
         receive snapshot
         Send OK
         recv Move request
         Send move to server
         Receive OK
        """
        # Request snapshot
        self.cmd_transaction(Command.REQUEST_SNAPSHOT)
        
        # receive snapshot
        snapshot = self.snapshot_transaction()
        
        # Show snapshot to user
        self.gfx.show_snapshot(snapshot)
        
        # Await Move request
        pl("recv request from server. Move?")
        
        cmd = self.recv_cmd()
        if not cmd == Command.REQUEST_MOVE:
            raise Exception("Server didn't request move")
        elif not cmd or cmd == '':
            pl("recv: connection closed unexpectedly")
            done = True
        elif cmd == Command.REQUEST_MOVE:
            pl("got move request")
            # Get move from player
            pass
        else:
            raise Exception("Client did not understand server request")
        # Send move to server
        self.mov_transaction(Move.ROCK)
        

    def end_match(self):
        """
         send OK
         recv snapshot
         send OK
         recv final snapshot
         send OK
        """        
        pl("Ending match")
        pl("sending OK")
        self.send_cmd(Command.OK)
        pl("Receive snapshot")
        snapshot = self.recv_snapshot()
        pl("sending OK")
        self.send_cmd(Command.OK)
        pl("show snapshot")
        self.gfx.show_snapshot(snapshot)
        pl("Recv final snapshot")
        winner = self.recv_final_snapshot()
        self.send_cmd(Command.OK)
        self.gfx.show_player_won(winner)
        pl("Client ended match")

    def recv_final_snapshot(self):
        msg = self.sock.recv(1024)
        msg = msg.decode('ascii')
        winner = Player("client")
        winner.unpack_from_string(msg)
        return winner
            
    def main_game_loop(self):
        done = False
        while not done:
            # Check to see if we are game
            # Or if we are done with the match
            self.send_cmd(Command.MATCH_OVER)
            cmd = self.recv_cmd()
            if cmd == Command.MATCH_OVER:
                done = True
                self.end_match()
            elif cmd == Command.OK:
                self.play_turn()
            else:
                raise Exception("Server is drunk.")
            
    def setup(self):
        pl("setting up client...")
        self.connect()
        self.send_player(self.player)
        cmd = self.recv_cmd()
        if not cmd == Command.OK:
            raise Exception("Server didn't respond with OK on connect")
        
if __name__ == '__main__':
    p = Player("client")
    cli = RPSXClient(host=socket.gethostname(),player = p)
    cli.setup()
    try:
        cli.play()
    except KeyboardInterrupt:
        pl("received interrupt")
        cli.tear_down()
    except:
        pl("something bad happened")
        cli.tear_down()
        raise
