import socket
import threading
import random
import time

host = ("localhost", 8091)
vazao = 8000 # bps
distancia = 10 # metros
proberro = 10 # 0-100%
timeout = 1
pktsize = 5 # tamanho do pacote
mspeed = 2 * 10**8 # velocidade do meio (fibra otica)
janela = 7 # qtd pacotes da janela
atraso = (pktsize/vazao) + (distancia/mspeed)

##################################################
# Atraso de transmissao (Dtrans) = L / R =>
#   quantidade de tempo pro router "empurrar" o pa
#   cote, nada a ver com distancia fisica dos routers
# L = tamanho do pacote (bits)
# R = banda do enlace (bps)
#
# Atraso de propagacao (Dprop) = S / v =>
#   tempo que 1 bit leva pra se propagar de um router
#   a outro
# S = distancia do enlace (metros)
# v = velocidade do meio de propagacao (~2x10^8 m/s)
#
# Atraso nodal (Dnodal) = Dtrans + Dprop
##################################################


##################################################
# Calc atraso =
# atraso = ((pktsize)/vazao) + (distancia/2*10^8)
##################################################

class srepeat():
    def __init__(self):
        self.initialize()

    def initialize(self):
        conn = connection_sr()
        nextwindow = [0] * janela # janela a ser enviada
        timeouts = [0] * janela # timeout de cada pacote da janela
        ackedpackets = [False] * janela # pacotes ja ACK
        for index in range(0,janela):
            nextwindow[index] = random.randint(0,255)
            timeouts[index] = time.time() + timeout

        conn.send_window(nextwindow, timeouts, ackedpackets) # envia a primeira janela
        while True:
            #time.sleep(timeout)
            conn.recv_msg(ackedpackets)

            isAllAcked = True
            for i,isAcked in enumerate(ackedpackets):
                if(not isAcked):
                    isAllAcked = False
                    if(timeouts[i] + 2 < time.time()): # se ja passou o timeout do pacote, reenvia
                        conn.send_individual_packet(i, nextwindow[i], timeouts, ackedpackets)

            if(isAllAcked): # se todos ja foram enviados, muda janela
                for index in range(0,janela):
                    nextwindow[index] = random.randint(0,255)
                    timeouts[index] = time.time() + timeout
                    ackedpackets[index] = False
                    
                conn.send_window(nextwindow, timeouts, ackedpackets)


class connection_sr():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = (atraso * 2)
        self.sock.settimeout(timeout)

    def send_window(self, nextwindow, timeouts, ackedpackets): # enviar os N pacotes da janela
        for index,packet in enumerate(nextwindow):
            failsend = random.randint(0,100)
            if (failsend >= proberro): # se n der erro, envia
                tosend = str(index) + " " + str(packet) # envia "X MSG"
                self.sock.sendto(tosend.encode(), host)
                timeouts[index] = time.time() + timeout
                ackedpackets[index] = False
                print("Pacote #" + str(index) + " (" + str(packet) + ") enviado")

    def send_individual_packet(self, i, packet, timeouts, ackedpackets):
        failsend = random.randint(0,100)
        if (failsend >= proberro):
            tosend = str(i) + " " + str(packet)
            self.sock.sendto(tosend.encode(), host)
            timeouts[i] = time.time() + timeout
            ackedpackets[i] = False
            print("Pacote #" + str(i) + " (" + str(packet) + ") reenviado")

    def recv_msg(self, ackedpackets): # retorna mensagem
        try:
            msg, server = self.sock.recvfrom(pktsize)
            print("Recebido " + msg.decode())
            arr_msg = msg.decode().split(" ") # recebe X ACK
            
            identifier = int(arr_msg[0])
            ackedpackets[identifier] = True
            return
        except socket.timeout:
            return


class stopnwait():
    def __init__(self):
        self.initialize()

    def initialize(self):
        conn = connection_snw()
        msg = str(random.randint(0,255))
        last_sent = False # ultima mensagem enviada tem identificador 0, inicialmente
        conn.send_msg(msg, last_sent)
        recvd_msg = None
        while True:
            time.sleep(timeout)
            (identifier, rmsg) = conn.recv_msg()
            if rmsg == None or identifier == last_sent: # se nao receber a msg (timeout) ou se o ACK nao bater com o da msg
                conn.send_msg(msg, last_sent)
            else:
                msg = str(random.randint(0,255))
                last_sent = not last_sent
                conn.send_msg(msg, last_sent)

class connection_snw():
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout = (2 * atraso)
        self.sock.settimeout(timeout)

    def send_msg(self, msg, ls):
        msg = ("1" if ls else "0") + " " + msg
        failsend = random.randint(0,100)
        print("#" + msg + " enviado")
        if(failsend > proberro): # se nao houver erro na transmissao da mensagem
            self.sock.sendto(msg.encode(), host)
        else:
            print("ocorreu um erro na transmissao")

    def recv_msg(self):
        try:
            msg, server = self.sock.recvfrom(pktsize)
            recvmsg = msg.decode().split(" ")
            print("#" + recvmsg[0] + " " + recvmsg[1] + " recebido")
            return (recvmsg[0], recvmsg[1])
        except socket.timeout:
            return (None, None)

    def close(self):
        self.sock.close()

mapp = stopnwait()