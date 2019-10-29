import socket
import threading
import random
import time

host = ("localhost", 8091)
vazao = 8000 # bps
distancia = 10 # metros
proberro = 0 # 0-100%
timeout = 1

class main():
    def __init__(self):
        self.initialize()

    def initialize(self):
        conn = connection()
        msg = str(random.randint(0,255))
        last_sent = False # ultima mensagem enviada tem identificador 0, inicialmente
        conn.send_msg(msg, last_sent)
        recvd_msg = None
        while True:
            time.sleep(timeout)
            (identifier, rmsg) = conn.recv_msg()
            if rmsg == None or identifier == last_sent:
                conn.send_msg(msg, last_sent)
            else:
                msg = str(random.randint(0,255))
                last_sent = not last_sent
                conn.send_msg(msg, last_sent)

class connection():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)
        print("Conectado")

    def send_msg(self, msg, ls):
        msg = ("1" if ls else "0") + " " + msg
        self.sock.sendto(msg.encode(), host)
        print("#" + msg + " enviado")

    def recv_msg(self):
        try:
            msg, server = self.sock.recvfrom(5)
            recvmsg = msg.decode().split(" ")
            print(recvmsg[1] + " recebido")
            return (recvmsg[0], recvmsg[1])
        except socket.timeout:
            return (None, None)

    def close(self):
        self.sock.close()

mapp = main()