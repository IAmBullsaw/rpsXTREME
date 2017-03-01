class Server:
    
    def listen(self):
        pass
    
    def start(self):
        done = False
        while not done:
            connection = self.listen()
            
if __name__ == '__main__':
    server = Server()
    server.start()
