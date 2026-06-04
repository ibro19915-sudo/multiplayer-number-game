import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5555

clients = {}
names = {}
moves = {}
scores = {1: 0, 2: 0}

lock = threading.Lock()


def send_all(message):
    for conn in list(clients.values()):
        try:
            conn.sendall((message + "\n").encode())
        except Exception:
            pass


def handle_client(conn, player_id):
    try:
        conn.sendall("ENTER_NAME\n".encode())
        name = conn.recv(1024).decode().strip()

        if not name:
            conn.close()
            return

        with lock:
            names[player_id] = name

        conn.sendall(
            f"Welcome {name}! Waiting for other player...\n".encode()
        )

        while True:
            data = conn.recv(1024)
            if not data:
                break

            move = data.decode().strip().upper()
            if move in ("ROCK", "PAPER", "SCISSORS"):
                with lock:
                    if player_id not in moves:
                        moves[player_id] = move
    except Exception:
        pass
    finally:
        conn.close()


def get_winner(move1, move2):
    if move1 == move2:
        return 0

    if (
        (move1 == "ROCK" and move2 == "SCISSORS")
        or (move1 == "PAPER" and move2 == "ROCK")
        or (move1 == "SCISSORS" and move2 == "PAPER")
    ):
        return 1

    return 2


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("RPS V4 Server Started")
print("Waiting for Player 1...")

conn1, addr1 = server.accept()
clients[1] = conn1
threading.Thread(target=handle_client, args=(conn1, 1), daemon=True).start()
print("Player 1 connected")
print("Waiting for Player 2...")

conn2, addr2 = server.accept()
clients[2] = conn2
threading.Thread(target=handle_client, args=(conn2, 2), daemon=True).start()
print("Player 2 connected")

while len(names) < 2:
    time.sleep(0.1)

send_all("")
send_all("====================")
send_all("ROCK PAPER SCISSORS V4")
send_all("====================")
send_all(f"Player 1: {names[1]}")
send_all(f"Player 2: {names[2]}")
send_all("")
send_all("First player to reach 3 wins!")

while scores[1] < 3 and scores[2] < 3:
    with lock:
        moves.clear()

    send_all("")
    send_all("====================")
    send_all(f"ROUND {scores[1] + scores[2] + 1}")
    send_all("====================")
    send_all("Choose:")
    send_all("ROCK")
    send_all("PAPER")
    send_all("SCISSORS")

    while True:
        with lock:
            if len(moves) == 2:
                break
        time.sleep(0.1)

    move1 = moves[1]
    move2 = moves[2]

    send_all("")
    send_all(f"{names[1]} chose {move1}")
    send_all(f"{names[2]} chose {move2}")

    winner = get_winner(move1, move2)

    if winner == 0:
        send_all("")
        send_all("DRAW!")
    else:
        scores[winner] += 1
        send_all("")
        send_all(f"{names[winner]} wins the round!")

    send_all("")
    send_all("SCOREBOARD")
    send_all(f"{names[1]}: {scores[1]}")
    send_all(f"{names[2]}: {scores[2]}")
    send_all("")

send_all("====================")
send_all("MATCH OVER")
send_all("====================")

if scores[1] > scores[2]:
    winner_name = names[1]
elif scores[2] > scores[1]:
    winner_name = names[2]
else:
    winner_name = "Nobody"

send_all(f"Winner: {winner_name}")
send_all("")
send_all("Final Score")
send_all(f"{names[1]}: {scores[1]}")
send_all(f"{names[2]}: {scores[2]}")

for conn in clients.values():
    try:
        conn.close()
    except Exception:
        pass
server.close()