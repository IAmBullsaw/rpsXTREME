import sys
from time import sleep
sys.path.insert(0, '../game')

import socket
from player import Player
debug = True

def pl(msg):
    if debug:
        print("\t" + msg)

class RPSXClient:
    def __init__(self, host='155.4.151.254', port=4711, player = player):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.player = player

    def connect(self):
        pl("Connecting to {}:{}".format(self.host,self.port))
        try:
            self.sock.connect((self.host,self.port))
        except Exception e:
            pl("Couldn't establish connection")
            raise e

    def close(self):
        pl("Closing connection to {}:{}".format(self.host,self.port))
        self.sock.close()
        
    def send_player(self,player):
        msg = player.pack_to_string()
        self.sock.send(msg.encode('ascii'))
        self.recv_cmd()

    def recv_start_match_data(self):
        pl("recv_start_match_data")
        msg = self.sock.recv(1024)
        pl(msg.decode('ascii'))

    def request_match(self):
        msg = "lfg"
        self.sock.send(msg.encode('ascii'))

    def recv_command(self):
        cmd = self.sock.recv(5)
        cmd = cmd.decode('ascii')
        ans = ''
        done = False
        if cmd == 'ok':
            ans = cmd
            
        return ans, done

    def play(self):
        done = False
        while not done:
            self.recv_command()

    def setup(self):
        cli.send_player(self.player)
        sleep(1)
        cli.request_match()
if __name__ == '__main__':
    p = Player("client")
    cli = RPSXClient(host=socket.gethostname(),player = p)
    cli.setup()
    cli.play()
    #cli.recv_start_match_data()
    cli.close()
