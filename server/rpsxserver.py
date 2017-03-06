import socket
import sys
import os
from timeit import default_timer as timer
from random import randint
from time import sleep

# When running as a script cwd is not script dir.
# Change cwd to dir where this file is...
os.chdir(os.path.dirname(__file__))

sys.path.insert(0,'../game')
from rpsxtreme import RPSXGame
from judge import Judge
from player import Player
from enums import Command, Move

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

    def __init__(self,host,port = 4711, connections = 5, turns_per_match = 5):
        self.server_socket = None
        self.host = host
        self.port = port
        self.connections = connections
        self.players = []
        self.uid = 0
        self.muid = 0
        self.start_time = None
        self.total_players = 0
        self.turns_per_match = turns_per_match
        
        ok = self.setup_server()
        if not ok:
            raise "Server not OK"

    def welcome(self):
        message = "Welcome to the rpsXtreme server"
        pl("*"*(len(message) + 22))
        pl("*" + " "*10 + message + " "*10 + "*")
        pl("*"*(len(message) + 22))

    def goodbye(self):
        message = "Goodbye for now..."
        uptime = (timer() - self.start_time)/60
        message2 = "Uptime: {} minutes".format(str(uptime))
        message3 = "Total players: {}".format(self.total_players)

        length = len(message2) + 22
        l = length - len(message) - 2
        l /= 2
        l = int(l)
        pl("*"*(length))
        pl("*" + " "*l + message + " "*l + "*")
        pl("*" + " "*10 + message2 + " "*10 + "*")
        l = length - len(message3) - 2
        l /= 2
        l = int(l)
        pl("*" + " "*l + message3 + " "*l + "*")
        pl("*"*(length))
        
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
        pl("Closing connection to {}".format(str(uid) if uid else str(cs) ))
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
        pl('Players online: {}'.format(len(self.players)))
        
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
        self.start_time = timer()
        self.welcome()
        pl("waiting for connections...")
        done = False
        while not done:
            try:
                client_socket, addr = self.server_socket.accept()
                pl("connection from {}".format(str(addr)))
                self.total_players += 1 # statistics only
                self.handle_connection(client_socket,addr)
            except (KeyboardInterrupt, SystemExit):
                done = True
                pl("caught interrupt")
                self.tear_down()
            except:
                pl("something bad happened")
                done = True
                self.tear_down()
                raise

    def tear_down(self):
        pl("tearing down server")
        self.close_all_client_sockets()
      
        pl("closing server socket")
        self.server_socket.close()
        self.server_socket = None
        
        self.goodbye()

    def close_all_client_sockets(self):
        pl("closing all sockets")
        for entry in self.players:
            self.send_cmd(entry[2], Command.CLOSE)
            sleep(0.05)
            entry[2].close()

    def handle_connection(self,cs,addr):
        pl("handling connection with {}".format(str(addr)))

        # Receive connected users player
        p = self.recv_player(cs)
        uid = self.create_unique_id()
        # Add player to players
        self.players.append((uid,p,cs,addr))
        
        #pl(str(self.players), len(self.players))

        # We received player and set up our part correctly, send OK
        self.send_cmd(cs,Command.OK)
        
        # User speaks to server
        done = False
        while not done:
            cmd = self.recv_cmd(cs)
            ans, done = self.cmd_to_instructions(cmd)
            exec(ans)

        # User is done with this session
        self.close_connection(cs = cs)

    def handle_match_request(self,cs,p):
        pl('handling match request from {}'.format(str(p)))
        if self.has_players():
            pl('setting up normal match...')
            raise Exception(NotImplemented)
        else:
            pl('setting up bot match...')
            p2 = Player("Gunhilda",bot=True)
            match = RPSXGame(p, p2, Judge(), bot=True)
            self.send_cmd(cs,Command.OK)
            
            pl('match set up')
            self.handle_bot_match(cs,match,p2)

    def handle_bot_match(self,cs,match,p2):
        pl("Handling bot match")
        done = False
        while not done:
            pl("Waiting for question")
            
            cmd = self.recv_cmd(cs)
            if not cmd == Command.MATCH_OVER:
                raise Exception("Client should wonder if match is over")
            else:
                if match.get_turns() >= self.turns_per_match:
                    # We are done with match
                    done = True
                else:
                    # We continue with match
                    self.send_cmd(cs, Command.OK)
                    self.play_turn(cs,match,p2)
        # When done
        
        pl("Server is ending match")
        pl("send: Command.MATCH_OVER")
        self.send_cmd(cs, Command.MATCH_OVER)
        self.handle_end_match(cs,match)
        pl("Bot match ended")
                    
                
    def play_turn(self,cs,match,p2):
        """
         Await a request for snapshot
         Send OK
         Send snapshot
         Receive OK
         Send Request move
         Receive move
         Send OK
        """
        pl("await snapshot")
        cmd = self.recv_cmd(cs)
        if not cmd == Command.REQUEST_SNAPSHOT:
            pass #:(
        # Send OK
        pl("send ok")
        self.send_cmd(cs,Command.OK)
        sleep(0.01)
        # Send snapshot
        pl("send snapshot")
        self.send_match_snapshot(cs,match.get_snapshot())
        sleep(0.1)
        #Receive OK
        pl("receive OK")
        cmd = self.recv_cmd(cs)
        if not cmd == Command.OK:
            raise Exception("client is not OK with snapshot")
        sleep(1)
        # Send Request move
        pl("send move request")
        self.send_cmd(cs,Command.REQUEST_MOVE)
        # Receive move
        pl("receive move")
        p1_mov = self.recv_mov(cs)
        
        # Send OK
        pl("send ok")
        self.send_cmd(cs,Command.OK)

        # Get bot move:
        #p2_mov = p2.get_chosen_move()
        #if p2move:
        #    match.set_p2move(p2_mov)
        # play the turn
        match.set_p1_move(p1_mov)
        match.play()
            

    def handle_end_match(self,cs,match):
        """
         recv OK
         send snapshot
         recv OK
         send final snapshot
         
        """

        # Did client get message?
        pl("receive OK")
        cmd = self.recv_cmd(cs)
        if not cmd == Command.OK:
            raise Exception("client did not get Command.MATCH_OVER")

        # Send snapshot
        self.send_match_snapshot(cs,match.get_snapshot())

        # Did client get snapshot?
        pl("receive OK")
        cmd = self.recv_cmd(cs)
        if not cmd == Command.OK:
            raise Exception("client is not OK with final snapshot")

        # Finish the match
        match.finish()

        # Send final snapshot (Winner)
        winner = match.get_winner()
        if winner:
            self.send_final_snapshot(cs,winner.pack_to_string())
        else:
            self.send_final_snapshot(cs,'DRAW')

        # Did client get winner?
        pl("receive OK")
        cmd = self.recv_cmd(cs)
        if not cmd == Command.OK:
            raise Exception("client is not OK with final snapshot")
        
                    
    def recv_cmd(self,cs):
        pl('waiting for command...')        
        cmd = cs.recv(10)
        cmd = Command.decode(cmd)
        pl("recv: {}".format(cmd))
        return cmd

    def recv_mov(self,cs):
        pl("waiting for move...")
        mov = cs.recv(10)
        mov = Move.decode(mov)
        pl("recv: {}".format(mov))
        return mov

    def cmd_to_instructions(self,cmd):
        ans = 'self.unknown_cmd()'
        done = False
        # Is connection closed?
        if cmd == 0 or not cmd or cmd == '' or cmd == None:
            pl('recv: connection was closed')
            ans = ''
            done = True
        # What was the command?
        else:
            if cmd == Command.CLOSE:
                pl('recv: CLOSE')
                ans = ''
                done = True
            elif cmd == Command.REQUEST_GAME:
                pl('recv: REQUEST_GAME')
                ans = 'self.handle_match_request(cs,p)'
            else:
                pl('recv: unknown cmd: {}'.format(cmd))
                ans = 'self.unknown_cmd()'
        return ans, done

    def send_cmd(self,cs,cmd):
        pl("send: '{}' to '{}'".format(cmd,str(cs.getpeername())))
        cs.send(cmd.encode('ascii'))

    def cmd_transaction(self,cs,send_cmd,ans_cmd = Command.OK):
        pl("Transaction: send {} recv{}".format(send_cmd,ans_cmd))
        self.send_cmd(send_cmd)
        cmd = self.recv_cmd(cs)
        if not cmd or cmd == '':
            pl("Transaction failed. Connection closed unexpectedly")
        if not cmd == ans_cmd:
            raise Exception("Transaction failed. Expected {} received {}".format(send_cmd,ans_cmd))
        
    def has_players(self):
        return len(self.players) > 1

    def unknown_cmd(self):
        pass

    def send_match_snapshot(self,cs,snapshot):
        pl("sending snapshot...")
        cs.send(snapshot.encode('ascii'))

    def send_final_snapshot(self,cs,snapshot):
        pl("sending final snapshot")
        cs.send(snapshot.encode('ascii'))
        
if __name__ == '__main__':
    server = RPSXServer(socket.gethostname())
    server.run()
