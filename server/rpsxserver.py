import socket

debug = True


def pl(message,t=True):
    if debug:
        if t:
            print("\t" + message)
        else:
            print(message)

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
        ok = self.setup_server()
        if not ok:
            raise "Server not OK"
        else:
            self.welcome()

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

    def handle_connection(self,cs,addr):
        pl("handling connection with {}".format(str(addr)))
        message = 'Thank you for connecting' + "\r\n"
        cs.send(message.encode('ascii'))

        pl("Closing connection to {}".format(str(addr)))
        cs.close()

    def run(self):
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
    
if __name__ == '__main__':
    server = RPSXServer(socket.gethostname())
    server.run()
