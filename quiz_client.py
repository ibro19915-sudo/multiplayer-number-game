import socket
import threading

player_id = 0


def listen(sock):
    global player_id

    while True:
        try:
            data = sock.recv(4096).decode()

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

        except:
            break


ip = input("Server IP: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, 5555))

threading.Thread(
    target=listen,
    args=(client,),
    daemon=True
).start()

while True:

    command = input().strip().upper()

    if command in ["A", "B", "C", "D", "SKIP"]:

        client.send(
            f"ANSWER:{command}\n".encode()
        )

    else:
        print(
            "Enter A, B, C, D or SKIP"
        )