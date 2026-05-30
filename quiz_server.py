import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5555

questions = [
    {
        "question": "What is the tallest building in the world?",
        "options": ["A) Eiffel Tower", "B) Burj Khalifa", "C) Big Ben", "D) CN Tower"],
        "answer": "B"
    },
    {
        "question": "What is the largest animal on Earth?",
        "options": ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Shark"],
        "answer": "B"
    },
    {
        "question": "What is the highest mountain in the world?",
        "options": ["A) K2", "B) Nanga Parbat", "C) Mount Everest", "D) Kilimanjaro"],
        "answer": "C"
    },
    {
        "question": "What is the largest ocean?",
        "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"],
        "answer": "D"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A) Mars", "B) Venus", "C) Jupiter", "D) Mercury"],
        "answer": "A"
    },
    {
        "question": "How many continents are there?",
        "options": ["A) 5", "B) 6", "C) 7", "D) 8"],
        "answer": "C"
    },
    {
        "question": "Which continent is the largest?",
        "options": ["A) Africa", "B) Europe", "C) Asia", "D) Australia"],
        "answer": "C"
    },
    {
        "question": "What is Earth's natural satellite?",
        "options": ["A) Mars", "B) Moon", "C) Venus", "D) Sun"],
        "answer": "B"
    },
    {
        "question": "Which country has the largest population?",
        "options": ["A) USA", "B) India", "C) Pakistan", "D) Brazil"],
        "answer": "B"
    },
    {
        "question": "What is the fastest land animal?",
        "options": ["A) Cheetah", "B) Lion", "C) Horse", "D) Leopard"],
        "answer": "A"
    }
]


clients = {}
scores = {1: 0, 2: 0}

answers = {}
locked_players = set()

lock = threading.Lock()

question_open = False
question_winner = None


def send_all(msg):
    for conn in clients.values():
        try:
            conn.send((msg + "\n").encode())
        except:
            pass


def handle_client(conn, player_id):
    global question_winner

    conn.send(f"PLAYER:{player_id}\n".encode())

    while True:
        try:
            data = conn.recv(1024).decode().strip()

            if not data:
                break

            if not data.startswith("ANSWER:"):
                continue

            answer = data.split(":", 1)[1].upper()

            with lock:

                if not question_open:
                    conn.send("Question closed.\n".encode())
                    continue

                if player_id in locked_players:
                    conn.send(
                        "You already answered or skipped.\n".encode()
                    )
                    continue

                locked_players.add(player_id)

                if answer == "SKIP":
                    answers[player_id] = "SKIP"
                    conn.send(
                        "You skipped this question.\n".encode()
                    )
                    continue

                answers[player_id] = answer

                current_question = questions[current_q]

                if (
                    question_winner is None
                    and answer == current_question["answer"]
                ):
                    question_winner = player_id
                    scores[player_id] += 1

                    send_all(
                        f"PLAYER {player_id} ANSWERED CORRECTLY FIRST!"
                    )

        except:
            break

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Quiz Server Running...")
print("Waiting for Player 1 and Player 2...")

for player_id in [1, 2]:
    conn, addr = server.accept()

    clients[player_id] = conn

    threading.Thread(
        target=handle_client,
        args=(conn, player_id),
        daemon=True
    ).start()

    print(f"Player {player_id} connected")

send_all("Both players connected!")
time.sleep(2)

for current_q in range(len(questions)):

    with lock:
        answers = {}
        locked_players = set()
        question_open = True
        question_winner = None

    q = questions[current_q]

    send_all("")
    send_all("=" * 40)
    send_all(f"QUESTION {current_q + 1}")
    send_all("=" * 40)
    send_all(q["question"])

    for option in q["options"]:
        send_all(option)

    # 15 second timer

    for sec in range(15, 0, -1):

        if sec == 10:
            send_all("⚠ 10 seconds remaining!")

        if sec == 5:
            send_all("⚠ 5 seconds remaining!")

        time.sleep(1)

    with lock:
        question_open = False

    send_all("")
    send_all(f"Correct Answer: {q['answer']}")

    if question_winner is None:
        send_all("Nobody answered correctly first.")
    else:
        send_all(
            f"Point awarded to Player {question_winner}"
        )

    send_all(
        f"SCORES -> P1: {scores[1]} | P2: {scores[2]}"
    )

    time.sleep(3)

send_all("")
send_all("=" * 40)
send_all("FINAL SCORES")
send_all("=" * 40)

send_all(f"Player 1: {scores[1]}")
send_all(f"Player 2: {scores[2]}")

if scores[1] > scores[2]:
    send_all("WINNER: PLAYER 1")
elif scores[2] > scores[1]:
    send_all("WINNER: PLAYER 2")
else:
    send_all("DRAW!")

print("Game Finished")