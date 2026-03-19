import msvcrt

print("Press keys (ESC to exit):")

while True:
    if msvcrt.kbhit():
        key = msvcrt.getwch()
        print("Key pressed:", repr(key))
        if key == '\x1b':  # ESC
            break
