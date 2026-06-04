import socket
import threading

player_name = ""


def listen(sock):

    global player_name

    while True:

        try:

            data = sock.recv(
                4096
            ).decode()

            if not data:
                break

            lines = data.split("\n")

            for line in lines:

                if not line.strip():
                    continue

                if line == "ENTER_NAME":

                    player_name = input(
                        "Enter your name: "
                    )

                    sock.send(
                        player_name.encode()
                    )

                else:

                    print(line)

        except:
            break


ip = input(
    "Server IP: "
)

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(
    (ip, 5555)
)

threading.Thread(
    target=listen,
    args=(client,),
    daemon=True
).start()

while True:

    move = input().strip().upper()

    if move in [
        "ROCK",
        "PAPER",
        "SCISSORS"
    ]:

        client.send(
            move.encode()
        )

    else:

        print(
            "Use ROCK, PAPER or SCISSORS"
        )