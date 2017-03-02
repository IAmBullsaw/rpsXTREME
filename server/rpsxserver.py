import socket

debug = True

def p(message):
    if debug:
        print(message)
            
if __name__ == '__main__':
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 5002
    p("binding socket to host {}, port {}".format(str(host),str(port)))
    server_socket.bind((host,port))
    server_socket.listen(5)
    p("listening to 5 connections.")
    done = False
    while not done:
        client_socket, addr = server_socket.accept()

        print("got a connection from {}".format(str(addr)))
        message = 'Thank you for connecting' + "\r\n"
        client_socket.send(message.encode('ascii'))
        client_socket.close()
