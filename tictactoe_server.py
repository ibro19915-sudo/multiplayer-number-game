import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

board = [" "] * 9
current_turn = 1
game_over = False

clients = {}
lock = threading.Lock()

WIN_COMBINATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


def board_string():
    return "".join(board)


def send_state(conn):
    try:
        conn.send(f"BOARD:{board_string()}\n".encode())
        conn.send(f"TURN:{current_turn}\n".encode())

        if game_over:
            conn.send("GAMEOVER\n".encode())
    except:
        pass


def broadcast():
    for c in list(clients.values()):
        send_state(c)


def winner():
    for combo in WIN_COMBINATIONS:
        a, b, c = combo

        if (
            board[a] != " "
            and board[a] == board[b]
            and board[b] == board[c]
        ):
            return board[a]

    return None


def board_full():
    return " " not in board


def handle_client(conn, player_id):
    global current_turn
    global game_over
    global board

    symbol = "X" if player_id == 1 else "O"

    print(f"Player {player_id} connected")

    conn.send(f"PLAYER:{player_id}\n".encode())

    send_state(conn)

    while True:
        try:
            data = conn.recv(1024).decode().strip()

            if not data:
                break

            if data == "RESTART":
                with lock:
                    board = [" "] * 9
                    current_turn = 1
                    game_over = False

                broadcast()
                continue

            if data.startswith("MOVE:"):

                try:
                    pos = int(data.split(":")[1]) - 1
                except:
                    conn.send("Invalid move\n".encode())
                    continue

                with lock:

                    if game_over:
                        conn.send("Game over\n".encode())
                        continue

                    if player_id != current_turn:
                        conn.send("Not your turn\n".encode())
                        continue

                    if pos < 0 or pos > 8:
                        conn.send("Position must be 1-9\n".encode())
                        continue

                    if board[pos] != " ":
                        conn.send("Square already used\n".encode())
                        continue

                    board[pos] = symbol

                    win = winner()

                    if win:
                        game_over = True

                        for c in clients.values():
                            c.send(f"WINNER:{win}\n".encode())

                    elif board_full():
                        game_over = True

                        for c in clients.values():
                            c.send("DRAW\n".encode())

                    else:
                        current_turn = 2 if current_turn == 1 else 1

                broadcast()

        except:
            break

    print(f"Player {player_id} disconnected")

    conn.close()

    if player_id in clients:
        del clients[player_id]


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Check every second so Ctrl+C works immediately
server.settimeout(1)

print("TicTacToe server running...")

player_id_counter = 0

try:
    while True:
        try:
            conn, addr = server.accept()
        except socket.timeout:
            continue

        if len(clients) >= 2:
            conn.send("Game full\n".encode())
            conn.close()
            continue

        player_id_counter += 1

        player_id = player_id_counter

        clients[player_id] = conn

        threading.Thread(
            target=handle_client,
            args=(conn, player_id),
            daemon=True
        ).start()

except KeyboardInterrupt:
    print("\nServer stopped by user.")

finally:
    for conn in list(clients.values()):
        try:
            conn.close()
        except:
            pass

    server.close()
    print("Server socket closed.")