import socket
import threading

player_id = 0
board = [" "] * 9


def draw_board():

    print()
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}")
    print()


def listen(sock):
    global player_id
    global board

    buffer = ""

    while True:
        try:
            data = sock.recv(1024).decode()

            if not data:
                break

            buffer += data

            while "\n" in buffer:

                line, buffer = buffer.split("\n", 1)

                if line.startswith("PLAYER:"):
                    player_id = int(line.split(":")[1])

                    symbol = "X" if player_id == 1 else "O"

                    print()
                    print(f"You are Player {player_id}")
                    print(f"Your symbol is {symbol}")

                elif line.startswith("BOARD:"):

                    raw = line.split(":", 1)[1]

                    board = list(raw)

                    draw_board()

                elif line.startswith("TURN:"):

                    turn = int(line.split(":")[1])

                    print(f"Turn: Player {turn}")

                elif line.startswith("WINNER:"):

                    winner = line.split(":")[1]

                    print()
                    print(f"Winner is {winner}")
                    print("Type RESTART to play again")

                elif line == "DRAW":

                    print()
                    print("Draw")
                    print("Type RESTART to play again")

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

print()
print("TIC TAC TOE")
print("Positions:")
print("1 2 3")
print("4 5 6")
print("7 8 9")
print()

while True:

    move = input("Move (1-9) or RESTART: ").strip()

    if move.upper() == "RESTART":
        client.send("RESTART\n".encode())
        continue

    if move not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        print("Enter 1-9")
        continue

    client.send(f"MOVE:{move}\n".encode())