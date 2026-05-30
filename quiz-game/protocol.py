import socket

def send_msg(conn: socket.socket, msg: str) -> None:
    try:
        conn.send((msg + "\n").encode())
    except Exception:
        pass

def recv_lines(conn: socket.socket, bufsize: int = 4096) -> str:
    try:
        data = conn.recv(bufsize).decode()
        return data
    except Exception:
        return ""
