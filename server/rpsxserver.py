import socket

debug = True


def p(message):
    if debug:
        print(message)


class RPSXServer:

    def __init__(self,host,port = 4711):
        self.server_socket = None
        self.host = host
        self.port = port
        ok = self.setup_server()
        if not ok:
            raise "Server not OK"

    def setup_server(self):
        p("setting up server")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        p("binding socket to host {}, port {}".format(str(self.host),str(self.port)))
        try:
            self.server_socket.bind((self.host,self.port))
        except:
            return False
        n = 5
        self.server_socket.listen(n)
        p("listening to max {} connections.".format(n))
        return True

    def handle_connection(self,cs,addr):
        p("handling connection...")
        message = 'Thank you for connecting' + "\r\n"
        cs.send(message.encode('ascii'))
        cs.close()
        p("handled connection...")

    def run(self):
        done = False
        while not done:
            try:
                client_socket, addr = self.server_socket.accept()
                print("got a connection from {}".format(str(addr)))
                self.handle_connection(client_socket,addr)
            except (KeyboardInterrupt, SystemExit):
                done = True
                self.quit()
            except:
                p("something bad happened")
                done = True
                self.quit()
                raise

    def quit(self):
        p("tearing down server")
        
        self.server_socket.close()
        self.server_socket = None
        p("closed socket")
    
if __name__ == '__main__':
    server = RPSXServer(socket.gethostname())
    server.run()
