import socket
import threading

HOST = "127.0.0.1"
PORT = 6000

shared_number = 0
clients = []
lock = threading.Lock()

# ----------- SERVER LOGIC -----------
def handle_client(conn):
    global shared_number

    # Send initial state
    conn.send(str(shared_number).encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            with lock:
                if data == "+":
                    shared_number += 1
                elif data == "-":
                    shared_number -= 1

                # Broadcast updated state
                for c in clients:
                    c.send(str(shared_number).encode())

        except:
            break

    clients.remove(conn)
    conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Server started. Waiting for connections...")

    while True:
        conn, addr = s.accept()
        clients.append(conn)
        threading.Thread(
            target=handle_client,
            args=(conn,),
            daemon=True
        ).start()

# ----------- CLIENT LOGIC -----------
def listen_server(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            print(f"\rShared number: {data}    \n(+ to add, - to subtract)", end="")
        except:
            break

def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    threading.Thread(
        target=listen_server,
        args=(s,),
        daemon=True
    ).start()

    while True:
        cmd = input()
        if cmd in ["+", "-"]:
            s.send(cmd.encode())

# ----------- ENTRY POINT -----------
mode = input("Server (s) or client (c)? ").lower()

if mode == "s":
    start_server()
else:
    start_client()
