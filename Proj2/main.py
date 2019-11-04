import client
import server
import time
from threading import *
from tkinter import *

class main(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()


    def initialize(self):
        self.resizable(0,0)
        self.grid()

        # container
        self.innerContainer = Frame(self)
        self.innerContainer.grid(column=0, row=1, padx=10, pady=10)

        self.labelTitle = Label(self, text="Insira os parâmetros:")
        self.labelTitle.config(font=(70))
        self.labelTitle.grid(column=0, row=0, pady=10)

        # vazao parametro
        self.defaultValue = StringVar(self.innerContainer, value="8000")
        self.labelVazao = Label(self.innerContainer, text="Vazão (bps):")
        self.inputVazao = Entry(self.innerContainer, width=50, textvariable=self.defaultValue)

        # distancia parametro
        self.defaultValue = StringVar(self.innerContainer, value="10")
        self.labelDistancia = Label(self.innerContainer, text="Distancia (metros):")
        self.inputDistancia = Entry(self.innerContainer, width=50, textvariable=self.defaultValue)

        # tamanho janela
        self.defaultValue = StringVar(self.innerContainer, value="7")
        self.labelJanela = Label(self.innerContainer, text="Tamanho da janela (pacotes. SR apenas):")
        self.inputJanela = Entry(self.innerContainer, width=50, textvariable=self.defaultValue)

        # prob erro
        self.defaultValue = StringVar(self.innerContainer, value="10")
        self.labelErro = Label(self.innerContainer, text="Probabilidade de erro (0-100):")
        self.inputErro = Entry(self.innerContainer, width=50, textvariable=self.defaultValue)

        # botao start SNW
        self.btnSWN = Button(self, text="Iniciar Stop-and-Wait", command=self.startStopnWait, width=20)
        # botao start SR
        self.btnSR = Button(self, text="Iniciar Selective Repeat", command=self.startSelectiveRepeat, width=20)
        # botao Stop
        #self.btnSTOP = Button(self, text="Parar", command=self.stopActivities, width=20)

        self.inputVazao.grid(column=1, row=1)
        self.labelVazao.grid(column=0, row=1)
        self.labelDistancia.grid(column=0, row=2)
        self.inputDistancia.grid(column=1, row=2)
        self.labelJanela.grid(column=0, row=3)
        self.inputJanela.grid(column=1, row=3)
        self.labelErro.grid(column=0, row=4)
        self.inputErro.grid(column=1, row=4)
        self.btnSWN.grid(column=0, row=2)
        self.btnSR.grid(column=0, row=3, pady=(0,10))

    def startStopnWait(self):
        server.vazao = int(self.inputVazao.get())
        server.distancia = int(self.inputDistancia.get())
        server.janela = int(self.inputJanela.get())
        server.atraso = int(self.inputErro.get())

        client.vazao = int(self.inputVazao.get())
        client.distancia = int(self.inputDistancia.get())
        client.janela = int(self.inputJanela.get())
        client.atraso = int(self.inputErro.get())

        t = Thread(target=self.startSNWServer)
        t.start()
        time.sleep(1)
        t2 = Thread(target=self.startSNWClient)
        t2.start()

    def startSNWServer(self):
        server.stopnwait()
    
    def startSNWClient(self):
        client.stopnwait()
    
    def startSelectiveRepeat(self):
        server.vazao = int(self.inputVazao.get())
        server.distancia = int(self.inputDistancia.get())
        server.janela = int(self.inputJanela.get())
        server.atraso = int(self.inputErro.get())

        client.vazao = int(self.inputVazao.get())
        client.distancia = int(self.inputDistancia.get())
        client.janela = int(self.inputJanela.get())
        client.atraso = int(self.inputErro.get())

        #self.btnSTOP.grid(column=0, row=4, pady=(0,10))

        try:
            t = Thread(target=self.startSRServer)
            t.start()
            time.sleep(1)
            t2 = Thread(target=self.startSRClient)
            t2.start()
        except (KeyboardInterrupt, SystemExit):
            print("ended")

    def startSRServer(self):
        server.srepeat()

    def startSRClient(self):
        client.srepeat()

m = main(None)
m.title("ARQ")
m.mainloop()
