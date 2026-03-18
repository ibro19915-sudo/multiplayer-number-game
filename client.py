import socket
import threading

HOST = input("Enter server IP (127.0.0.1 for same PC): ")
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

player_id = None

print("\n=== NUMBER GAME ===")
print("Goal: Reach 10 to win")
print("On your turn, type: ADD:1 or ADD:2")
print("Commands:")
print("CREATE:CODE")
print("JOIN:CODE")
print("ADDBOTS:CODE:NUMBER\n")


def listen():
    global player_id

    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break

            for line in msg.split("\n"):
                if not line:
                    continue

                if line.startswith("You are Player"):
                    player_id = int(line.split()[-1])
                    print(f"\n>>> You are Player {player_id}")

                elif line.startswith("NUMBER:"):
                    print(f"\nCurrent Number: {line.split(':')[1]}")

                elif line.startswith("TURN:"):
                    turn = int(line.split(":")[1])
                    if player_id == turn:
                        print(">>> Your turn!")
                    else:
                        print(f"Waiting... Player {turn}")

                elif line.startswith("STATUS:"):
                    status = line.split(":")[1]

                    if "WINS" in status:
                        print(f"\n=== {status} ===")
                        if str(player_id) in status:
                            print("🎉 You WIN!")
                        else:
                            print("😢 You lose")
                        print("Type RESTART to play again")

                    else:
                        print(f"Game Status: {status}")

                else:
                    print(line)

        except:
            print("Disconnected")
            break


def send():
    while True:
        try:
            msg = input()
            client.send(msg.encode())
        except:
            break


threading.Thread(target=listen).start()
send()
