import json

HEADER_SIZE = 4

def send_message(sock, message):
    body = json.dumps(message).encode("utf-8")  
    header = len(body).to_bytes(HEADER_SIZE, "big")  
    sock.sendall(header + body)   

def recv_exactly(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if chunk == b"":
            raise ConnectionError("the other side closed the connection")
        data += chunk
    return data

def recv_message(sock):
    header = recv_exactly(sock, HEADER_SIZE)   
    size = int.from_bytes(header, "big")
    body = recv_exactly(sock, size)
    return json.loads(body.decode("utf-8"))
