import socket
from protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 5000

def handle_command(command):
    """Look at the command's "acao" and build the response dict."""
    action = command.get("acao")
    args = command.get("args", {})

    if action == "ECHO":
        result = {"ok": True, "texto": args.get("texto", "")}
    else:
        result = {"ok": False, "erro": f"unknown action: {action}"}

    return {
        "id": command.get("id"),
        "tipo": "resposta",
        "acao": action,
        "resultado": result,
    }


def serve_one_controller(conn, addr):
    """Talk to one connected controller until it disconnects."""
    print(f"*** THIS MACHINE IS UNDER REMOTE CONTROL by {addr[0]}:{addr[1]} ***")
    try:
        while True:
            command = recv_message(conn)
            print(f"received: {command}")
            response = handle_command(command)
            send_message(conn, response)
    except (ConnectionError, ValueError) as e:
        print(f"session ended: {e}")
    finally:
        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()
    print(f"agent listening on port {PORT} (Ctrl+C to quit)")

    try:
        while True:
            conn, addr = server.accept()
            serve_one_controller(conn, addr)
            print("waiting for next controller...")
    except KeyboardInterrupt:
        print("agent stopped")
    finally:
        server.close()


if __name__ == "__main__":
    main()
