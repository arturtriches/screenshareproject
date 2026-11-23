import socket
def server(ip = "localhost", port=8082):
    payload = 2048 
    sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    addr = (ip, port)
    sock.bind(addr)
    sock.listen(5) 

    for i in range(2):
        client, addr = sock.accept()
        got = client.recv(payload)
        if got:
            print(f" - {got}")
            client.send(got)
            print(f"mandou {got} bytes de volta pra {addr}")
            client.close()
server()