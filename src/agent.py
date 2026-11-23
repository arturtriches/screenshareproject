import socket
from protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 5000

def handle_command(command):
    action = command.get("acao")
    args = command.get("args", {})

    match action:
        case "ECHO":
            result = {"ok": True, "texto": args.get("texto", "")}
        case "EXEC":
            result = {"ok": True,}
        case _:
            result = {"ok": False, "erro": f"acao desconhecida: {action}"}

    return {
        "id": command.get("id"),
        "tipo": "resposta",
        "acao": action,
        "resultado": result,
    }

def serve_one_controller(conn, addr):
    print(f"*** ESSA MAQUINA ESTA SENDO CONTROLADA POR {addr[0]}:{addr[1]} ***")
    try:
        while True:
            command = recv_message(conn)
            print(f"recebeu: {command}")
            response = handle_command(command)
            send_message(conn, response)
    except (ConnectionError, ValueError) as e:
        print(f"sessao finalizada: {e}")
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()
    print(f"escutando na porta {PORT} (Ctrl+C pra sair)")

    try:
        while True:
            conn, addr = server.accept()
            serve_one_controller(conn, addr)
            print("esperando proximo controlador")
    except KeyboardInterrupt:
        print("parou")
    finally:
        server.close()

if __name__ == "__main__":
    main()
