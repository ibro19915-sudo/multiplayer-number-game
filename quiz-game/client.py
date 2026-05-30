import socket
import threading
import argparse

from protocol import recv_lines, send_msg


def listen(sock: socket.socket):
    player_id = 0
    while True:
        data = recv_lines(sock)
        if not data:
            break

        lines = data.split("\n")
        for line in lines:
            if not line.strip():
                continue

            if line.startswith("PLAYER:"):
                player_id = int(line.split(":")[1])
                print()
                print(f"You are Player {player_id}")
                print("Commands:")
                print("A, B, C, D = Answer")
                print("SKIP = Skip question")
                print()
            else:
                print(line)


def main():
    parser = argparse.ArgumentParser(description="Quiz client")
    parser.add_argument("server", help="Server IP or hostname")
    parser.add_argument("--port", default=5555, type=int)
    args = parser.parse_args()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.server, args.port))

    threading.Thread(target=listen, args=(client,), daemon=True).start()

    while True:
        command = input().strip().upper()
        if command in ["A", "B", "C", "D", "SKIP"]:
            send_msg(client, f"ANSWER:{command}")
        else:
            print("Enter A, B, C, D or SKIP")


if __name__ == "__main__":
    main()
