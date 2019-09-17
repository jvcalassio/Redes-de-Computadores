import socket
import ssl
import json
import tkinter
import threading


class app(tkinter.Tk):

    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
    # Monta a interface grafica
    def initialize(self):
        self.resizable(0, 0)
        self.grid()
        self.minsize(350, 100)

        self.label_Link = tkinter.Label(
            self, text="Insert video URL:")  # label
        self.label_Link.grid(column=0, row=0, padx=10, pady=(10, 5))

        self.container = tkinter.Frame(self)  # input + button frame
        self.container.grid(column=0, row=1, padx=8, pady=5)

        self.entry_Link = tkinter.Entry(self.container, width=50)  # input
        #self.entry_Link.grid(column = 0, row = 1, padx = (10,3), pady = 5)
        self.entry_Link.pack(side="left", padx=5)
        self.bind("<Return>", (lambda event: self.SearchCall()))

        self.button_Search = tkinter.Button(self.container, text="Search", command=self.SearchCall)  # button
        #self.button_Search.grid(column = 1, row = 1, padx = (0,10))
        self.button_Search.pack(side="right", padx=1)

        self.label_Views = tkinter.Label(self, text="")  # response
        self.label_Views.grid(column=0, row=2, pady=3)
        
    # Chamada da funcao de busca em outra thread (e o programa nao ficar travado)
    def SearchCall(self):
        t = threading.Thread(target=self.Search)
        t.start()
        self.label_Views["text"] = "Loading..."

    # Realiza a validacao da URL inserida. Se correta, realiza a busca
    def Search(self):
        try:
            yt_valid = [
                "youtube.com/watch?v",
                "http://youtube.com/watch?v",
                "http://www.youtube.com/watch?v",
                "www.youtube.com/watch?v",
                "https://youtube.com/watch?v",
                "https://www.youtube.com/watch?v"
            ]
            link_video = str(self.entry_Link.get()).split("=")

            if(link_video[0] not in yt_valid):
                raise(IndexError("invalid"))
            
            id_video = link_video[1].split("&")[0]

            if(id_video == ""):
                raise(IndexError("invalid"))

            self.label_Views["text"] = self.return_data(self.get_data(id_video))
        except IndexError:
            self.label_Views["text"] = "Invalid URL. Please provide a full YouTube URL:\nhttps://www.youtube.com/watch?v=xxxxxxxx"

    # Realiza a conexao com o servidor
    def get_data(self, id_video):
        try:
            hostname = "www.googleapis.com"
            addr = (hostname, 443) # porta 443 = TLS/SSL
            request = b"GET /youtube/v3/videos?part=statistics%2Csnippet&id="
            request += bytes(id_video.encode("utf-8"))
            request += b"&key=AIzaSyBaXGIGJzo3cVv-I5gUlz4Mbydoa_SzB_Q"
            request += b"&fields=items(snippet(title),statistics(viewCount)) "
            request += b"HTTP/1.1\r\n"
            request += b"Host: www.googleapis.com\r\n"
            request += b"Accept: application/json\r\n\r\n"

            timeout = 5 # tempo limite escolhido para sobrar tempo de recebimento dos pacotes

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) # conexao TCP
            sock.settimeout(timeout)

            ssock = ssl.wrap_socket(sock, server_side=False, ssl_version=ssl.PROTOCOL_TLS) # protecao do socket
            ssock.connect(addr)
            ssock.sendall(request)

            str_headers = ssock.recv()  # headers ignorados
            str_json = ""
            while True:
                try:
                    str_json += ssock.recv().decode("utf-8")
                except socket.timeout:
                    break

            ssock.close()
            sock.close()
            return str_json
        except socket.timeout:
            return None

    # Tratamento do JSON recebido e exibicao da mensagem na tela
    def return_data(self, str_json):
        if(str_json != None):
            try:
                dec_json = json.loads(str_json)
                titulo_video = dec_json["items"][0]["snippet"]["title"]
                qtd_views = int(dec_json["items"][0]["statistics"]["viewCount"])
                qtd_with_comma = f"{qtd_views:,d}"
            except IndexError:
                return "An error has occured. Please try again."
            except ValueError:
                return "An error has occured. Please try again."
            else:
                return "\"" + titulo_video + "\" has " + qtd_with_comma.replace(",", ".") + " views"
        else:
            return "An error has occured. Please try again."


meuapp = app(None)
meuapp.title("Youtube - Views")
meuapp.mainloop()
