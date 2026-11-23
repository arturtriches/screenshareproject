import socket
import sys
import uuid
from protocol import send_message, recv_message

PORT = 5000

def make_command(action, args):
    return {
        "id": str(uuid.uuid4()),
        "tipo": "comando",
        "acao": action,
        "args": args,
    }

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, PORT))
    print(f"connected to agent at {host}:{PORT}")

    try:
        while True:
            text = input("> ")
            if text == "sair":
                break
            command = make_command("ECHO", {"texto": text})
            send_message(sock, command)
            response = recv_message(sock)
            print(f"agent answered: {response['resultado']}")
    except ConnectionError as e:
        print(f"lost connection: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
