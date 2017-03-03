import socket
import sys
from random import randint

sys.path.insert(0,'../game')
from player import Player

debug = True


def pl(message,t=True):
    if debug:
        if t:
            print("\t" + str(message))
        else:
            print(str(message))

def p(message,t=True):
    if debug:
        if t:
            print("\t" + message, end="")
        else:
            print(message, end="")
def pdot():
    if debug:
        print('.', end="")

class RPSXServer:

    def __init__(self,host,port = 4711, connections = 5):
        self.server_socket = None
        self.host = host
        self.port = port
        self.connections = connections
        self.players = []
        self.uid = 0
        self.muid = 0
        
        ok = self.setup_server()
        if not ok:
            raise "Server not OK"

    def welcome(self):
        message = "Welcome to the rpsXtreme server"
        pl("*"*(len(message) + 22))
        pl("*" + " "*10 + message + " "*10 + "*")
        pl("*"*(len(message) + 22))
        
    def setup_server(self):
        p("setting up server")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pdot()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        pdot()
        pl('')
        pl("binding socket to host {}, port {}".format(str(self.host),str(self.port)))
        try:
            self.server_socket.bind((self.host,self.port))
        except:
            return False
        self.server_socket.listen(self.connections)
        pl("listening to max {} connections".format(self.connections))
        return True

    def close_connection(self,uid = None, cs = None):
        pl("Closing connection to {}".format(str(uid)))
        if uid:
            for i,entry in enumerate(self.players):
                if entry[0] == uid:
                    entry[2].close()
                    self.remove_players_entry(i)
                    break
        elif cs:
            for i,entry in enumerate(self.players):
                if entry[2] == cs:
                    entry[2].close()
                    self.remove_players_entry(i)
                    break
        else:
            pl('uid = {}, cs = {}'.format(str(uid),str(cs)))                    

    def remove_players_entry(self,i):
        self.players.pop(i)
        pl(len(self.players))
        
    def recv_player(self,cs):
        msg = cs.recv(1024)
        player = Player("Server")
        player.unpack_from_string(msg.decode('ascii'))
        return player

    def recv_move(self,cs):
        msg = cs.recv(1024)
        pl(msg.decode('ascii'))

    def create_unique_id(self):
        uid = self.uid
        self.uid = self.uid + 1
        return uid

    def create_match_uid(self):
        muid = self.muid
        self.muid = self.muid + 1
        return muid
    
    def run(self):
        self.welcome()
        pl("waiting for connections...")
        done = False
        while not done:
            try:
                client_socket, addr = self.server_socket.accept()
                pl("connection from {}".format(str(addr)))
                self.handle_connection(client_socket,addr)
            except (KeyboardInterrupt, SystemExit):
                done = True
                pl("caught interrupt")
                self.quit()
            except:
                pl("something bad happened")
                done = True
                self.quit()
                raise

    def quit(self):
        pl("tearing down server")
        
        self.server_socket.close()
        self.server_socket = None
        pl("closed socket")

    def handle_connection(self,cs,addr):
        pl("handling connection with {}".format(str(addr)))

        p = self.recv_player(cs)
        uid = self.create_unique_id()
        self.players.append((uid,p,cs,addr))
        pl(str(self.players), len(self.players))

        done = False
        while not done:
            ans = self.recv_cmd(cs)
            eval(ans)

        self.close_connection(cs)

    def handle_match_request(self,cs,p):
        pl('handling match request from {}'.format(str(p)))
        if self.has_players():
            pass
        else:
            pl('setting up bot match...')
        
    def recv_cmd(self,cs):
        cmd = cs.recv(5)

        if not cmd:
            return 'done = True'
        
        cmd = str(cmd.decode('ascii'))
        ans = 'self.unknown_cmd()'
        pl('cmd == ' + cmd)
        if cmd == 'q':
            pl('q was requested')
            ans = 'done = True'
        elif cmd == 'lfg':
            pl('lfg was requested')
            ans = 'self.handle_match_request(cs,p)'
        else:
            pl('unknown cmd')
            ans = 'self.unknown_cmd()'
        return ans

    def has_players(self):
        return len(self.players) > 1

    def unknown_cmd(self):
        pass
    
if __name__ == '__main__':
    server = RPSXServer(socket.gethostname())
    server.run()
