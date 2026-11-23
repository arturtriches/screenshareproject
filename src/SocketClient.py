import socket

def conectar(ip,port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (ip,port)

    client.connect(addr)
    try:
        msg = str(input("insira mensagem: "))
        client.sendall(msg.encode('utf-8'))

        got = 0
        wanted = len(msg)
        while got < wanted:
            new = client.recv(32)
            got+=len(new)
            print(f"- {new}")

    except socket.error as e:
        print(e)
    finally:
        client.close()
conectar("localhost",8082)

