import socket
import threading
import msvcrt

HOST = "127.0.0.1"
PORT = 5000

typing_sent = False

# ---------- RECEIVE ----------
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                print("\nConnection closed.")
                return

            if data == "__TYPING__":
                print("\rFriend is typing...   ", end="\r")
            elif data == "__STOP__":
                print("\r" + " " * 30 + "\r", end="")
            else:
                print(f"\rFriend: {data}\nYou: ", end="")
        except:
            return

# ---------- SEND ----------
def send_messages(sock):
    global typing_sent
    buffer = ""

    print("You: ", end="", flush=True)

    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()

            # First key ? send typing signal
            if not typing_sent:
                try:
                    sock.send(b"__TYPING__")
                except:
                    print("\nConnection closed.")
                    return
                typing_sent = True

            # ENTER ? send message
            if ch == "\r":
                print()
                try:
                    sock.send(b"__STOP__")
                    sock.send(buffer.encode())
                except:
                    print("\nConnection closed.")
                    return
                buffer = ""
                typing_sent = False
                print("You: ", end="", flush=True)

            # BACKSPACE
            elif ch == "\b":
                if buffer:
                    buffer = buffer[:-1]
                    print("\b \b", end="", flush=True)

            # NORMAL CHAR
            else:
                buffer += ch
                print(ch, end="", flush=True)

# ---------- MAIN ----------
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    mode = input("Host (h) or connect (c)? ").lower()
    if mode == "h":
        s.bind((HOST, PORT))
        s.listen(1)
        print("Waiting for connection...")
        conn, addr = s.accept()
        print("Connected.")
    else:
        s.connect((HOST, PORT))
        conn = s

    threading.Thread(
        target=receive_messages,
        args=(conn,),
        daemon=True
    ).start()

    send_messages(conn)

if __name__ == "__main__":
    main()
