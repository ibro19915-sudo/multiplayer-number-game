import socket
import threading
import random
import string
import os

HOST = "0.0.0.0"
PORT = 5555

lock = threading.Lock()

# ========== GAME CLASS ==========
class Game:
    def __init__(self, code):
        self.code = code
        self.players = {}   # id -> conn
        self.next_player_id = 1
        self.current_number = 0
        self.current_turn = 1
        self.status = "PLAYING"
        self.file = f"game_{code}.txt"
        self.load_state()

    def load_state(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    data = f.read().split(",")
                    self.current_number = int(data[0])
                    self.current_turn = int(data[1])
                    self.status = data[2]
            except:
                pass

    def save_state(self):
        with open(self.file, "w") as f:
            f.write(f"{self.current_number},{self.current_turn},{self.status}")

    def broadcast(self):
        for c in self.players.values():
            try:
                c.send(f"NUMBER:{self.current_number}\n".encode())
                c.send(f"TURN:{self.current_turn}\n".encode())
                c.send(f"STATUS:{self.status}\n".encode())
            except:
                pass

games = {}

# ========== HANDLE CLIENT ==========
def handle_client(conn, addr):
    global games

    player_id = None
    game = None

    try:
        conn.send("Welcome! Use CREATE:CODE or JOIN:CODE\n".encode())

        while True:
            msg = conn.recv(1024).decode().strip()
            if not msg:
                break

            # ===== CREATE GAME =====
            if msg.startswith("CREATE:"):
                code = msg.split(":")[1]

                with lock:
                    if code in games:
                        conn.send("Game already exists\n".encode())
                        continue

                    game = Game(code)
                    games[code] = game

                    player_id = game.next_player_id
                    game.players[player_id] = conn
                    game.next_player_id += 1

                conn.send(f"You are Player {player_id}\n".encode())
                game.broadcast()
                continue

            # ===== JOIN GAME =====
            if msg.startswith("JOIN:"):
                code = msg.split(":")[1]

                with lock:
                    if code not in games:
                        conn.send("Game not found\n".encode())
                        continue

                    game = games[code]

                    player_id = game.next_player_id
                    game.players[player_id] = conn
                    game.next_player_id += 1

                conn.send(f"You are Player {player_id}\n".encode())
                game.broadcast()
                continue

            # ===== ADD BOTS =====
            if msg.startswith("ADDBOTS:"):
                _, code, count = msg.split(":")
                count = int(count)

                if code not in games:
                    conn.send("Game not found\n".encode())
                    continue

                game = games[code]

                for _ in range(count):
                    bot_id = game.next_player_id
                    game.players[bot_id] = None
                    game.next_player_id += 1

                conn.send(f"{count} bots added\n".encode())
                game.broadcast()
                continue

            # ===== RESTART =====
            if msg == "RESTART":
                with lock:
                    game.current_number = 0
                    game.current_turn = 1
                    game.status = "PLAYING"
                    game.save_state()
                game.broadcast()
                continue

            # ===== MOVE =====
            if msg.startswith("ADD:"):
                move = int(msg.split(":")[1])

                with lock:
                    if game.status != "PLAYING":
                        continue

                    if player_id != game.current_turn:
                        conn.send("Not your turn\n".encode())
                        continue

                    if move not in [1, 2]:
                        conn.send("Invalid move\n".encode())
                        continue

                    game.current_number += move

                    if game.current_number >= 10:
                        game.status = f"PLAYER {player_id} WINS"
                    else:
                        game.current_turn += 1
                        if game.current_turn >= game.next_player_id:
                            game.current_turn = 1

                    game.save_state()

                game.broadcast()

                # ===== BOT AUTO PLAY =====
                run_bots(game)

    except:
        pass

    conn.close()

# ========== BOT SYSTEM ==========
def run_bots(game):
    while True:
        with lock:
            if game.current_turn not in game.players:
                return

            if game.players[game.current_turn] is not None:
                return  # human turn

            if game.status != "PLAYING":
                return

            move = random.choice([1, 2])
            game.current_number += move

            if game.current_number >= 10:
                game.status = f"PLAYER {game.current_turn} WINS"
            else:
                game.current_turn += 1
                if game.current_turn >= game.next_player_id:
                    game.current_turn = 1

            game.save_state()

        game.broadcast()

# ========== START SERVER ==========
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Server running...")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()
