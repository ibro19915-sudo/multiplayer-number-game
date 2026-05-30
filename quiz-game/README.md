Quiz Game (modularized)
=======================

Run the server (wait for two players):

```bash
python server.py --host 0.0.0.0 --port 5555
```

Run a client (connect to server IP):

```bash
python client.py 127.0.0.1 --port 5555
```

Notes and next steps:
- `protocol.py` contains simple send/recv helpers. Replace with framing or JSON for reliability.
- `data.py` contains questions; consider loading from JSON/DB for scalability.
- Add a GUI frontend later (websocket + web UI) or richer CLI UX.
