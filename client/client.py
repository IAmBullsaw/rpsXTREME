import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '155.4.151.254'
port = 4711

print("Connecting to {}:{}".format(host,port))
sock.connect((host,port))
print("Recv")
msg = sock.recv(1024)
print("Close")
sock.close()

print(msg.decode('ascii'))
