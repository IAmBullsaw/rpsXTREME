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
    def __init__(self, host='155.4.151.254', port=4711):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        pl("Connecting to {}:{}".format(self.host,self.port))
        self.sock.connect((self.host,self.port))

    def close(self):
        pl("Closing connection to {}:{}".format(self.host,self.port))
        self.sock.close()
        
    def send_player(self,player):
        msg = player.pack_to_string()
        self.sock.send(msg.encode('ascii'))

    def recv_start_match_data(self):
        pl("recv_start_match_data")
        msg = self.sock.recv(1024)
        pl(msg.decode('ascii'))

    def request_match(self):
        msg = "lfg"
        self.sock.send(msg.encode('ascii'))
        
if __name__ == '__main__':
    p = Player("client")
    cli = RPSXClient(host=socket.gethostname())
    cli.connect()
    cli.send_player(p)
    sleep(1)
    cli.request_match()
    #cli.recv_start_match_data()
    cli.close()
