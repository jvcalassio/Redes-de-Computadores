import socket

host = ("localhost", 8091)

class main():
    def __init__(self):
        self.initialize()

    def initialize(self):
        sv = server()

class server():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(host)
        self.listen()

    def listen(self):
        while True:
            msg, cliente = self.sock.recvfrom(17)
            print("Mensagem recebida: " + msg.decode())
            identifier = msg.decode().split(" ")[0]
            self.sock.sendto((identifier + " ACK").encode(), cliente)

    def close(self):
        self.sock.close()

m = main()