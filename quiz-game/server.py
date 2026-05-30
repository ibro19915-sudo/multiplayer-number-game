import socket
import threading
import time
import argparse

from data import questions
from protocol import send_msg, recv_lines


class QuizServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 5555, max_players: int = 2):
        self.host = host
        self.port = port
        self.max_players = max_players
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = {}
        self.scores = {i + 1: 0 for i in range(max_players)}

        self.answers = {}
        self.locked_players = set()

        self.lock = threading.Lock()

        self.question_open = False
        self.question_winner = None

    def broadcast(self, msg: str):
        for conn in list(self.clients.values()):
            send_msg(conn, msg)

    def handle_client(self, conn: socket.socket, player_id: int):
        send_msg(conn, f"PLAYER:{player_id}")

        while True:
            data = recv_lines(conn)
            if not data:
                break

            for line in data.split("\n"):
                if not line.strip():
                    continue

                if not line.startswith("ANSWER:"):
                    continue

                answer = line.split(":", 1)[1].strip().upper()

                with self.lock:
                    if not self.question_open:
                        send_msg(conn, "Question closed.")
                        continue

                    if player_id in self.locked_players:
                        send_msg(conn, "You already answered or skipped.")
                        continue

                    self.locked_players.add(player_id)

                    if answer == "SKIP":
                        self.answers[player_id] = "SKIP"
                        send_msg(conn, "You skipped this question.")
                        continue

                    self.answers[player_id] = answer
                    # confirm receipt to the player
                    send_msg(conn, f"Answer recorded: {answer}")

                    current_question = questions[self.current_q]

                    # compare normalized answers (single-letter)
                    correct = current_question["answer"].strip().upper()
                    if self.question_winner is None and answer == correct:
                        self.question_winner = player_id
                        self.scores[player_id] += 1
                        self.broadcast(f"PLAYER {player_id} ANSWERED CORRECTLY FIRST!")

        conn.close()

    def accept_clients(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Quiz Server Running on {self.host}:{self.port}...")
        print(f"Waiting for {self.max_players} players...")

        for player_id in range(1, self.max_players + 1):
            conn, addr = self.server.accept()
            self.clients[player_id] = conn

            threading.Thread(target=self.handle_client, args=(conn, player_id), daemon=True).start()
            print(f"Player {player_id} connected from {addr}")

        self.broadcast("Both players connected!")

    def run_quiz(self):
        time.sleep(1)
        for self.current_q in range(len(questions)):
            with self.lock:
                self.answers = {}
                self.locked_players = set()
                self.question_open = True
                self.question_winner = None

            q = questions[self.current_q]

            self.broadcast("")
            self.broadcast("=" * 40)
            self.broadcast(f"QUESTION {self.current_q + 1}")
            self.broadcast("=" * 40)
            self.broadcast(q["question"])

            for option in q["options"]:
                self.broadcast(option)

            for sec in range(15, 0, -1):
                if sec == 10:
                    self.broadcast("⚠ 10 seconds remaining!")
                if sec == 5:
                    self.broadcast("⚠ 5 seconds remaining!")
                time.sleep(1)

            with self.lock:
                self.question_open = False

            self.broadcast("")
            self.broadcast(f"Correct Answer: {q['answer']}")

            if self.question_winner is None:
                self.broadcast("Nobody answered correctly first.")
            else:
                self.broadcast(f"Point awarded to Player {self.question_winner}")

            self.broadcast(f"SCORES -> " + " | ".join([f"P{i}: {self.scores[i]}" for i in sorted(self.scores)]))

            time.sleep(2)

        self.broadcast("")
        self.broadcast("=" * 40)
        self.broadcast("FINAL SCORES")
        self.broadcast("=" * 40)

        for i in sorted(self.scores):
            self.broadcast(f"Player {i}: {self.scores[i]}")

        if self.scores[1] > self.scores[2]:
            self.broadcast("WINNER: PLAYER 1")
        elif self.scores[2] > self.scores[1]:
            self.broadcast("WINNER: PLAYER 2")
        else:
            self.broadcast("DRAW!")

        print("Game Finished")

    def start(self):
        self.accept_clients()
        self.run_quiz()


def main():
    parser = argparse.ArgumentParser(description="Run quiz server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=5555, type=int)
    args = parser.parse_args()

    server = QuizServer(host=args.host, port=args.port)
    server.start()


if __name__ == "__main__":
    main()
