import sys
from time import sleep
sys.path.insert(0, '../game')

import socket
from player import Player
from enums import Command
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
        
    def recv_cmd(self):
        pl("waiting for command...")
        cmd = self.sock.recv(10)
        return Command.decode(cmd)

    def cmd_to_instructions(self,cmd):
        ans = ''
        done = False
        if not cmd or cmd == '':
            pl("recv: connection closed unexpectedly")
            ans = 'self.connection_lost()'
            done = True
        elif cmd == Command.OK:
            pl("recv: OK")
            ans = ''
        else:
            pl("recv: unknown command: {}".format(cmd))
            ans = 'raise Exception("Unknown command received")'
            done = True
        return ans, done

    def play(self):
        """
        1. send: request game
        2. recv: ok
        3. recv: get game
        
        while not done
        4. recv: get request for move
        5. send: move
        6. recv: ok
        7. recv: turn outcome / match outcome
        
        """
        pl("requesting game...")

        self.send_cmd(Command.REQUEST_GAME)
        cmd = self.recv_cmd()
        ans, done = self.cmd_to_instructions(cmd)
        if ans == '':
            pass # It was not OK :(
        
        
        done = False
        while not done:
            cmd = self.recv_cmd()
            ans, done = self.cmd_to_instructions(cmd)
            exec(ans)
        self.send_cmd(Command.CLOSE)
        self.tear_down()
        
    def setup(self):
        pl("setting up client...")
        self.connect()
        self.send_player(self.player)
        cmd = self.recv_cmd()
        ans, done = self.cmd_to_instructions(cmd)
        if not ans == '':
            exec(ans)
        
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
