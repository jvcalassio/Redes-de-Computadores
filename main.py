import socket, ssl, json, time

def get_data():
    hostname = "www.googleapis.com"
    addr = (hostname, 443)
    request = b"GET /youtube/v3/videos?part=statistics%2Csnippet&id=dQw4w9WgXcQ&key=AIzaSyBaXGIGJzo3cVv-I5gUlz4Mbydoa_SzB_Q "
    request += b"HTTP/1.1\r\n"
    request += b"Host: www.googleapis.com\r\n"
    request += b"Accept: application/json\r\n\r\n"
    timeout = 5

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.settimeout(timeout)

    ssock = ssl.wrap_socket(sock, server_side = False, ssl_version=ssl.PROTOCOL_TLS)
    ssock.connect(addr)
    ssock.sendall(request)

    str_headers = ssock.recv() # headers
    str_json = ""
    while True:
        try:
            str_json += ssock.recv().decode("utf-8")
        except socket.timeout:
            break;
        
    ssock.close()
    sock.close()
    return str_json

def print_data(str_json):
    dec_json = json.loads(str_json)
    titulo_video = dec_json["items"][0]["snippet"]["title"]
    qtd_views = int(dec_json["items"][0]["statistics"]["viewCount"])
    qtd_with_comma = f"{qtd_views:,d}"
    print("Visualizacoes do video \"" + titulo_video + "\": " + qtd_with_comma.replace(",","."))

while True:
    print_data(get_data())
    time.sleep(30)
    
