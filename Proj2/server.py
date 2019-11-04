import socket
import random
import time
import sys
from math import ceil

host = ("localhost", 8091)

vazao = 8000 # bps
distancia = 10 # metros
proberro = 10 # 0-100%
timeout = 1
pktsize = 5 # tamanho do pacote
mspeed = 2 * 10**8 # velocidade do meio (fibra otica)
janela = 7 # qtd pacotes da janela
atraso = (pktsize/vazao) + (distancia/mspeed)
delivered = []

class srepeat():
    def __init__(self):
        sv = server_sr()

class server_sr():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(ceil(atraso))
        self.sock.bind(host)
        print("Esperando mensagens")
        self.listen()

    def listen(self):
        buffer = [None] * janela
        delivered = []
        while True:
            try:
                #time.sleep(atraso)
                msg, cliente = self.sock.recvfrom(pktsize)
                print("Mensagem recebida: ", msg.decode())
                arr_msg = msg.decode().split(" ") # arr_msg[0] = codigo; 
                                                  # arr_msg[1] = msg;
                
                identifier = int(arr_msg[0])
                buffer[identifier] = arr_msg[1] # salva o pacote no buffer
                # envia ACK do pacote recebido
                failsend = random.randint(0,100)

                if(failsend >= proberro): # se nao cumprir a prob de erro
                    self.sock.sendto((arr_msg[0] + " ACK").encode(), cliente) # envia X ACK
                    print("ACK #" + arr_msg[0] + " enviado")
                else:
                    print("Erro ao enviar o ACK #" + arr_msg[0])

                complete = True
                for i,data in enumerate(buffer):
                    if(data == None):
                        complete = False

                if(complete): # janela completa, salva no delivered
                    delivered.append(buffer.copy())
                    for i in range(0,janela):
                        buffer[i] = None

            except socket.timeout:
                continue

            except KeyboardInterrupt:
                print(delivered)
                sys.exit()


class stopnwait():
    def __init__(self):
        sv = server_snw()

class server_snw():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(ceil(atraso))
        self.sock.bind(host)
        print("Esperando mensagens")
        self.listen()

    def listen(self):
        delivered = []
        while isRunning:
            try:
                msg, cliente = self.sock.recvfrom(pktsize)
                print("Mensagem recebida: " + msg.decode())
                identifier = msg.decode().split(" ")[0]
                failsend = random.randint(0,100)
                delivered.append(msg.decode().split(" ")[1])
                if(failsend > proberro): # se nao houver erro na transmissao do ack
                    self.sock.sendto((identifier + " ACK").encode(), cliente)
                else:
                    print("erro na transmissao do ACK " + identifier)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print(delivered)
                sys.exit()

    def close(self):
        self.sock.close()

#m = srepeat()