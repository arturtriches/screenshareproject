import socket, sys, uuid
from protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 5000

sys.stdout.reconfigure(errors="replace")

def make_command(action, args):
    return {
        "id": str(uuid.uuid4()),
        "tipo": "comando",
        "acao": action,
        "args": args,
    }

def request(sock, action, args):
    send_message(sock, make_command(action, args))
    return recv_message(sock)["resultado"]

def show_result(result):
    if not result["ok"]:
        print(f"erro: {result['erro']}")
        return
    print(result["stdout"], end="")
    if result["stderr"]:
        print(result["stderr"], end="")
    print(f"[codigo de saida: {result['codigo']}]")

def main():
    host = HOST

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, PORT))
    print(f"conectou em {host}:{PORT}")

    try:
        info = request(sock, "INFO", {})
        if info["ok"]:
            print(f"agente: {info['so']} {info['versao']} ({info['maquina']}), comandos vao pro {info['shell']}")
        while True:
            try:
                text = input("> ")
            except EOFError:
                break
            if text == "sair":
                break
            show_result(request(sock, "EXEC", {"cmd": text}))
    except ConnectionError as e:
        print(f"perdeu conexao: {e}")
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()

if __name__ == "__main__":
    main()
