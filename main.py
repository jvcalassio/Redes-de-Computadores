import socket, ssl, json, time

def get_data(id_video):
    try:
        hostname = "www.googleapis.com"
        addr = (hostname, 443)
        request = b"GET /youtube/v3/videos?part=statistics%2Csnippet&id="
        request += bytes(id_video.encode("utf-8"))
        request += b"&key=AIzaSyBaXGIGJzo3cVv-I5gUlz4Mbydoa_SzB_Q"
        request += b"&fields=items(snippet(title),statistics(viewCount)) "
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
    except socket.timeout:
        return None

def print_data(str_json):
    if(str_json != None):
        dec_json = json.loads(str_json)
        titulo_video = dec_json["items"][0]["snippet"]["title"]
        qtd_views = int(dec_json["items"][0]["statistics"]["viewCount"])
        qtd_with_comma = f"{qtd_views:,d}"
        print("Visualizacoes do video \"" + titulo_video + "\": " + qtd_with_comma.replace(",","."))


link_video = str(input()).split("=")
id_video = link_video[1].split("&")[0]

while True:
    print_data(get_data(id_video))
    time.sleep(30)
    
